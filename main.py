import glfw
from OpenGL.GL import *
from lorenz import LorenzSystem
import graphics_utils as gu 
import numpy as np
import math

# --- 1. USER INPUT SECTION (Before Window Initialization) ---
def get_user_configuration():
    print("====================================================")
    print("      LORENZ ATTRACTOR: THE BUTTERFLY EFFECT        ")
    print("====================================================")
    print("Standard Physical Parameters:")
    print("  - Sigma (σ) : 10.0  (Fluid buoyancy vs viscosity)")
    print("  - Rho (ρ)   : 28.0  (Temperature gradient)")
    print("  - Beta (β)  : 2.667 (Physical dimensions)")
    print("----------------------------------------------------")
    print("System A (Rainbow) starting point: (1.0, 1.0, 1.0)")
    
    # Get Epsilon
    try:
        eps = float(input("\nEnter Epsilon (Difference in Z for System B, e.g., 0.00001): "))
    except ValueError:
        print("Invalid input. Using default 0.00001")
        eps = 1e-5

    # Get Speed
    try:
        speed = int(input("Enter Simulation Speed (Steps per frame, e.g., 2 or 5): "))
    except ValueError:
        print("Invalid input. Using default 2")
        speed = 2
        
    print("\nStarting simulation... Press SPACE to pause/resume.")
    print("Use Mouse Left-Click to rotate and Scroll to zoom.")
    print("====================================================\n")
    return eps, speed

# Camera state
cam_yaw, cam_pitch, cam_dist = 45.0, 20.0, 120.0
mouse_last_x, mouse_last_y = 0, 0
first_mouse = True

def draw_lorenz_trail(lorenz_sys):
    """Helper function to handle circular buffer drawing logic."""
    if lorenz_sys.count < lorenz_sys.max_points:
        glDrawArrays(GL_LINE_STRIP, 0, lorenz_sys.count)
    else:
        start_idx = lorenz_sys.count % lorenz_sys.max_points
        glDrawArrays(GL_LINE_STRIP, start_idx, lorenz_sys.max_points - start_idx)
        glDrawArrays(GL_LINE_STRIP, 0, start_idx)

def main():
    global first_mouse, cam_yaw, cam_pitch, cam_dist, mouse_last_x, mouse_last_y
    
    # Collect inputs first
    epsilon, sim_speed = get_user_configuration()

    if not glfw.init(): return

    glfw.window_hint(glfw.SAMPLES, 8) 
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(1280, 720, "Lorenz Attractor - Comparison Analysis", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1) 

    # --- SIMULATION SETUP ---
    paused = False

    # System A (Standard)
    lorenz_a = LorenzSystem(initial_state=(1.0, 1.0, 1.0), max_points=40000, dt=0.005)
    # System B (Standard + Epsilon)
    lorenz_b = LorenzSystem(initial_state=(1.0, 1.0, 1.0 + epsilon), max_points=40000, dt=0.005)

    # Callbacks
    def key_cb(w, key, scancode, action, mods):
        nonlocal paused
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            paused = not paused
    glfw.set_key_callback(window, key_cb)

    def m_cb(w, x, y):
        global cam_yaw, cam_pitch, mouse_last_x, mouse_last_y, first_mouse
        if glfw.get_mouse_button(w, glfw.MOUSE_BUTTON_LEFT):
            if first_mouse: mouse_last_x, mouse_last_y = x, y; first_mouse = False
            cam_yaw += (x - mouse_last_x) * 0.2
            cam_pitch = max(min(cam_pitch + (mouse_last_y - y) * 0.2, 89), -89)
        else: first_mouse = True
        mouse_last_x, mouse_last_y = x, y
    
    glfw.set_cursor_pos_callback(window, m_cb)
    glfw.set_scroll_callback(window, lambda w, x, y: globals().update(cam_dist=max(10, cam_dist-y*5)))

    # OpenGL Configuration
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE) 
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Graphics Resources
    vao_a, vbo_a = gu.create_trajectory_buffer(lorenz_a.max_points)
    vao_b, vbo_b = gu.create_trajectory_buffer(lorenz_b.max_points)
    axes_vao, axes_count = gu.create_axes_buffer(80)
    shader = gu.create_shader_program()

    mvp_loc = glGetUniformLocation(shader, "MVP")
    solid_loc = glGetUniformLocation(shader, "uUseSolidColor")
    color_loc = glGetUniformLocation(shader, "uSolidColor")

    while not glfw.window_should_close(window):
        if not paused:
            # Use the pre-calculated sim_speed integer
            for _ in range(sim_speed):
                lorenz_a.step()
                lorenz_b.step()
            
            gu.update_vbo(vbo_a, lorenz_a.get_points())
            gu.update_vbo(vbo_b, lorenz_b.get_points())

        width, height = glfw.get_framebuffer_size(window)
        glViewport(0, 0, width, height)
        glClearColor(0.01, 0.01, 0.02, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Camera positioning
        eye = np.array([
            cam_dist * math.cos(math.radians(cam_yaw)) * math.cos(math.radians(cam_pitch)),
            cam_dist * math.sin(math.radians(cam_yaw)) * math.cos(math.radians(cam_pitch)),
            cam_dist * math.sin(math.radians(cam_pitch)) + 25
        ], dtype=np.float32)
        target = np.array([0, 0, 25], dtype=np.float32)
        view = gu.look_at(eye, target, np.array([0,0,1], dtype=np.float32))
        proj = gu.perspective(45.0, width/height, 0.1, 1000.0)
        mvp = (proj @ view).T

        glUseProgram(shader)
        glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, mvp)

        # 1. DRAW AXES
        glUniform1i(solid_loc, True)
        glUniform3f(color_loc, 0.2, 0.2, 0.2)
        glBindVertexArray(axes_vao)
        glDrawArrays(GL_LINES, 0, axes_count)

        # 2. DRAW LORENZ A (Rainbow)
        glUniform1i(solid_loc, False)
        glBindVertexArray(vao_a)
        draw_lorenz_trail(lorenz_a)

        # 3. DRAW LORENZ B (Comparison - White)
        glUniform1i(solid_loc, True)
        glUniform3f(color_loc, 1.0, 1.0, 1.0)
        glBindVertexArray(vao_b)
        draw_lorenz_trail(lorenz_b)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()