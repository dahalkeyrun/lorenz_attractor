import glfw
from OpenGL.GL import *

def main():
    # Initialize GLFW
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    # Create a window
    window_width, window_height = 800, 600
    window = glfw.create_window(window_width, window_height, "PyOpenGL Animation", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")

    # Make the OpenGL context current
    glfw.make_context_current(window)

    # Set background color
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Set up orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Main loop
    while not glfw.window_should_close(window):
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Example drawing: a white point in the center
        glColor3f(1.0, 1.0, 1.0)
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex2f(window_width / 2, window_height / 2)
        glEnd()

        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Clean up
    glfw.terminate()

if __name__ == "__main__":
    main()
