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
from models.lista_objetos import *

from transformacoes_mat.transforms import *

ALTURA = 700
LARGURA = 700   
TAM_CHAO = 60 
MARGEM = 2 #margem para não desenhar objetos muito próximos do limite do chão
QTD_ARVORES = 30

window = create_window(LARGURA, ALTURA)

ourShader = Shader("graficos/shaders/vertex_shader.vs", "graficos/shaders/fragment_shader.fs")
ourShader.use()

program = ourShader.getProgram()

load_objetos()  

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
polygonal_mode = False ## não esquecer de programar para ativar isso quando quise
glUniform1i(glGetUniformLocation(program, "imagem"), 0)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#definir posições das árvores
posicoes_arvores = []

for _ in range(QTD_ARVORES):  
    x = random.uniform(-TAM_CHAO + MARGEM, TAM_CHAO - MARGEM)
    z = random.uniform(-TAM_CHAO + MARGEM, TAM_CHAO - MARGEM)

    posicoes_arvores.append((x, z))

while not glfw.window_should_close(window):

    currentFrame = glfw.get_time()
    controls.deltaTime = currentFrame - controls.lastFrame
    controls.lastFrame = currentFrame

    glfw.poll_events() 
       
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glClearColor(0.0, 0.0, 0.1, 1.0) #cor do ceu
    
    if polygonal_mode:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    glActiveTexture(GL_TEXTURE0)

    desenha_opacos(program, True) 
    desenha_arvores(program, True, posicoes_arvores)
    desenha_transparentes(program, True)

    #mat = transformacoes();

    mat_view = view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    #mat_projection = perspective(45, LARGURA/LARGURA, 0.1, 100) #perspectiva

    mat_projection = projection(ALTURA, LARGURA)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    glfw.swap_buffers(window)

glfw.terminate()