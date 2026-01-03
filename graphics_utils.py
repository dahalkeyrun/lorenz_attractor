from OpenGL.GL import *

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