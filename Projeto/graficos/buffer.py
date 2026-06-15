import numpy as np
import ctypes
from OpenGL.GL import *


def setup_buffers(
    vertices_list,
    textures_coord_list,
    normals_list,
    program
):

    ####################################################
    # GERA 3 VBOs
    ####################################################

    # 0 -> vertices
    # 1 -> UV
    # 2 -> normais
    buffer_VBO = glGenBuffers(3)

    ####################################################
    # VÉRTICES
    ####################################################

    vertices = np.zeros(
        len(vertices_list),
        [("position", np.float32, 3)]
    )

    vertices["position"] = vertices_list

    glBindBuffer(
        GL_ARRAY_BUFFER,
        buffer_VBO[0]
    )

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
    )

    stride = vertices.strides[0]

    offset = ctypes.c_void_p(0)

    # location 0
    loc_vertices = 0

    glEnableVertexAttribArray(loc_vertices)

    glVertexAttribPointer(
        loc_vertices,
        3,
        GL_FLOAT,
        GL_FALSE,
        stride,
        offset
    )

    ####################################################
    # TEXTURAS (UV)
    ####################################################

    textures = np.zeros(
        len(textures_coord_list),
        [("position", np.float32, 2)]
    )

    textures["position"] = textures_coord_list

    glBindBuffer(
        GL_ARRAY_BUFFER,
        buffer_VBO[1]
    )

    glBufferData(
        GL_ARRAY_BUFFER,
        textures.nbytes,
        textures,
        GL_STATIC_DRAW
    )

    stride = textures.strides[0]

    offset = ctypes.c_void_p(0)

    # location 1
    loc_texture_coord = 1

    glEnableVertexAttribArray(loc_texture_coord)

    glVertexAttribPointer(
        loc_texture_coord,
        2,
        GL_FLOAT,
        GL_FALSE,
        stride,
        offset
    )

    ####################################################
    # NORMAIS
    ####################################################

    normals = np.zeros(
        len(normals_list),
        [("position", np.float32, 3)]
    )

    normals["position"] = normals_list

    glBindBuffer(
        GL_ARRAY_BUFFER,
        buffer_VBO[2]
    )

    glBufferData(
        GL_ARRAY_BUFFER,
        normals.nbytes,
        normals,
        GL_STATIC_DRAW
    )

    stride = normals.strides[0]

    offset = ctypes.c_void_p(0)

    # location 2
    loc_normals = 2

    glEnableVertexAttribArray(loc_normals)

    glVertexAttribPointer(
        loc_normals,
        3,
        GL_FLOAT,
        GL_FALSE,
        stride,
        offset
    )

    ####################################################
    # LIMPA BIND
    ####################################################

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return buffer_VBO