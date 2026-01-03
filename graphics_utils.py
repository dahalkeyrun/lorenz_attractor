from OpenGL.GL import *
import math
import numpy as np
from numpy import dtype
# shader source code 
VERTEX_SHADER_SOURCE = """
layout (location = 0) in vec3 aPos;
uniform mat4 MVP; // Model-View-Projection Matrix

void main() {
    // Transform the 3D Lorenz point to screen space
    gl_Position = MVP * vec4(aPos, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
out vec4 FragColor;
uniform vec3 uColor;

void main() {
    // Set the color of the line
    FragColor = vec4(uColor, 1.0);
}
"""

def perspective (fov, aspect, near, far):
    """Creates a prespective projection matrix"""
    f = 1.0/math.tan(math.radians(fov) / 2)
    matrix = np.zeros((4, 4), dtype=np.float32)
    matrix[0, 0] = f / aspect
    matrix[1, 1] = f
    matrix[2, 2] = (far + near) / (near - far)
    matrix[2, 3] = (2 * far * near) / (near - far)
    matrix[3, 2] = -1 

    return matrix


def look_at(eye, target, up):
    """creates a view matrix (the camera position/direction)"""
    f = (target - eye)
    f /= np.linalg.norm(f)
    s = np.cross(f, up)
    s /= np.linalg.norm(s)
    u = up.cross(s, f)

    m = np.identity(4, dtype=np.float32)
    m[0, :3] = s
    m[1, :3] = u
    m[2, :3] = -f

    t = np.identity(4, dtype=np.float32)
    t[:3, 3] = -eye

    return m @ t

def create_shader_program():
    #1. compile vertex shader
    vs = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vs, VERTEX_SHADER_SOURCE)
    glCompileShader(vs)

    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        raise RuntimeError(f"Vertex Shader Error: {glGetShaderInfoLog(vs).decode()}")

    # 2. compile fragment shader
    fs = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fs, FRAGMENT_SHADER_SOURCE)
    glCompileShader(fs)


    if not glGetShaderiv(fs, GL_COMPILE_STATUS):
        raise RuntimeError(f"Fragment Shader Error: {glGetShaderInfoLog(fs).decode()}")
    

    # 3. Linking shaders into a program
    program = glCreateProgram()
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)


    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(f"Shader linking error: {glGetProgramInfoLog(program).decode()}")
        

    glDeleteShader(vs)
    glDeleteShader(fs)

    return program



def create_trajectory_buffer(max_points):
    """
    Allocates memory on the GPU for the trajectory.
    Returns the VAO and VBO handles.
    """

    # creating and Binding VAO(Vertex Array Object)
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    #creating and Binding VBO(vertex Buffer Object)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    #allocating storage
    # max_points * 3(x,y,z) * 4 (float32 size)
    buffer_size = max_points * 3 * 4
    glBufferData(GL_ARRAY_BUFFER, buffer_size, None, GL_DYNAMIC_DRAW)

    # define attribute layout (location 0 = position)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)


    #Unbind
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    

    return vao, vbo


def update_vbo(vbo, points):
    '''
    streams numpy points data to the VBO.
    '''

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferSubData(GL_ARRAY_BUFFER, 0, points.nbytes, points)
    glBindBuffer(GL_ARRAY_BUFFER, 0)