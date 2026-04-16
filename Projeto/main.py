import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
from numpy import random
from PIL import Image

from graficos.shader_s import Shader
import camera.controls as controls
from camera.controls import *
from config.window import *
from graficos.buffer import *
from models.objetos import *

from transformacoes_mat.transforms import *

ALTURA = 700
LARGURA = 700   

window = create_window(LARGURA, ALTURA)

ourShader = Shader("graficos/shaders/vertex_shader.vs", "graficos/shaders/fragment_shader.fs")
ourShader.use()

program = ourShader.getProgram()

# carrega modelos (casa e vela): PARA TESTE POR ENQUANTO, DEPOIS VOU ORGANIZAR MELHOR ISSO AQUI
verticeInicial_casa, quantosVertices_casa, textura_casa = load_obj_and_texture(
    'objetos/casa/casa.obj',
    ['objetos/casa/texturas/casa.png']
)

verticeInicial_vela, quantosVertices_vela, textura_vela = load_obj_and_texture(
    'objetos/velas/velas.obj',
    ['objetos/velas/texturas/vela1.png']
)

verticeInicial_lanterna, quantosVertices_lanterna, textura_lanterna = load_obj_and_texture(
    'objetos/lanterna/lanterna.obj',
    ['objetos/lanterna/texturas/body_TT_checker_512x512_UV_GRID_BaseColor.jpg']
)

# CRIAR VAO (OBRIGATÓRIO no macOS / OpenGL Core)
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

buffer = setup_buffers(vertices_list, textures_coord_list, program)

def framebuffer_size_callback(window, largura, altura):

    # make sure the viewport matches the new window dimensions note that width and 
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, LARGURA, ALTURA)

# configurações de controle da câmera
glfw.set_key_callback(window,key_event)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
glfw.set_cursor_pos_callback(window, mouse_callback)
glfw.set_scroll_callback(window, scroll_callback)

# tell GLFW to capture our mouse
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

init_camera(LARGURA, ALTURA)

glfw.show_window(window)

glEnable(GL_DEPTH_TEST) ### importante para 3D
polygonal_mode = False 
glUniform1i(glGetUniformLocation(program, "imagem"), 0)

while not glfw.window_should_close(window):

    currentFrame = glfw.get_time()
    controls.deltaTime = currentFrame - controls.lastFrame
    controls.lastFrame = currentFrame

    glfw.poll_events() 
       
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if polygonal_mode:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    glActiveTexture(GL_TEXTURE0)

    desenha_objeto(program, verticeInicial_casa, quantosVertices_casa,
               0, 0, 1, 0, -20, -20, 0, 1, 1, 1,
               textura_casa[0])

    desenha_objeto(program, verticeInicial_vela, quantosVertices_vela,
               0, 0, 1, 0, 20, 20, 0, 1, 1, 1,
               textura_vela[0])
    desenha_objeto(program, verticeInicial_lanterna, quantosVertices_lanterna, 0, 0, 1, 0, -10, -10, 0, 0.7, 0.7, 0.7, textura_lanterna[0])

    mat_view = view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = projection(ALTURA, LARGURA)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    glfw.swap_buffers(window)

glfw.terminate()