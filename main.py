import glfw
from OpenGL.GL import *
from lorenz import LorenzSystem
from graphics_utils import create_trajectory_buffer, update_vbo, create_shader_program, look_at, perspective
import numpy as np
import math

# Global variables for camera
cam_yaw = 45.0
cam_pitch = 20.0
cam_dist = 100.0
mouse_last_x, mouse_last_y = 0, 0
first_mouse = True

def mouse_callback(window, xpos, ypos):
    global cam_yaw, cam_pitch, mouse_last_x, mouse_last_y, first_mouse
    if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        if first_mouse:
            mouse_last_x, mouse_last_y = xpos, ypos
            first_mouse = False
        
        dx = xpos - mouse_last_x
        dy = mouse_last_y - ypos # Reversed since y-coordinates go from bottom to top
        
        cam_yaw += dx * 0.2
        cam_pitch = max(min(cam_pitch + dy * 0.2, 89.0), -89.0)
        
    mouse_last_x, mouse_last_y = xpos, ypos

def scroll_callback(window, xoffset, yoffset):
    global cam_dist
    cam_dist = max(10.0, cam_dist - yoffset * 5.0)

def main():
    global first_mouse
    if not glfw.init(): return

    window = glfw.create_window(1000, 800, "Lorenz Attractor 3D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    
    # Modern OpenGL settings
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.02, 0.02, 0.05, 1.0) # Dark blue-black background

    lorenz = LorenzSystem(dt=0.005, max_points=20000) # More points for longer trail
    vao, vbo = create_trajectory_buffer(lorenz.max_points)
    shader_program = create_shader_program()
    
    mvp_loc = glGetUniformLocation(shader_program, "MVP")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 1. Update Simulation (run 2 steps per frame for speed)
        lorenz.step()
        lorenz.step()
        update_vbo(vbo, lorenz.get_points())

        # 2. Camera Logic (Orbiting)
        width, height = glfw.get_framebuffer_size(window)
        rad_yaw = math.radians(cam_yaw)
        rad_pitch = math.radians(cam_pitch)
        
        cx = cam_dist * math.cos(rad_yaw) * math.cos(rad_pitch)
        cy = cam_dist * math.sin(rad_yaw) * math.cos(rad_pitch)
        cz = cam_dist * math.sin(rad_pitch)
        
        target = np.array([0, 0, 25], dtype=np.float32)
        eye = target + np.array([cx, cy, cz], dtype=np.float32)
        
        view = look_at(eye, target, np.array([0, 0, 1], dtype=np.float32))
        proj = perspective(45.0, width/height, 0.1, 1000.0)
        mvp = (proj @ view).T # Transpose for OpenGL

        # 3. Render
        glUseProgram(shader_program)
        glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, mvp)
        
        glBindVertexArray(vao)
        glDrawArrays(GL_LINE_STRIP, 0, lorenz.count)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
        
        # Reset mouse state if button released
        if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.RELEASE:
            first_mouse = True

    glfw.terminate()

if __name__ == "__main__":
    main()