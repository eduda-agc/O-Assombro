import numpy as np
from OpenGL.GL import *

def setup_buffers(vertices_list, textures_coord_list, program):
    buffer_VBO = glGenBuffers(2)

    vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
    vertices['position'] = vertices_list


    # Upload data
    glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO[0])
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)
    loc_vertices = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc_vertices)
    glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

    textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
    textures['position'] = textures_coord_list


    # Upload data
    glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO[1])
    glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
    stride = textures.strides[0]
    offset = ctypes.c_void_p(0)
    loc_texture_coord = glGetAttribLocation(program, "texture_coord")

    glEnableVertexAttribArray(loc_texture_coord)
    glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)
    
    return buffer_VBO