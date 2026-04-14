import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
from numpy import random
from PIL import Image

from Projeto.graficos.shader_s import Shader

from Projeto.config.window import *
from Projeto.graficos.buffer import *
from Projeto.models.objetos import *
from Projeto.camera.controls import *
from Projeto.transformacoes_mat.transforms import *

ALTURA = 700
LARGURA = 700   

window = create_window(LARGURA, ALTURA)

ourShader = Shader("vertex_shader.vs", "fragment_shader.fs")
ourShader.use()

program = ourShader.getProgram()

# carrega caixa (modelo e texturas)
verticeInicial_caixa, quantosVertices_caixa = load_obj_and_texture('objetos/caixa/caixa.obj', ['objetos/caixa/caixa.jpg', 'objetos/caixa/tijolos.jpg', 'objetos/caixa/matrix.jpg'])

#objetos.py

buffer = setup_buffers(vertices_list, textures_coord_list)
# camera.py

# controls.py


glfw.show_window(window)

glEnable(GL_DEPTH_TEST) ### importante para 3D
polygonal_mode = False 

while not glfw.window_should_close(window):

    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame

    glfw.poll_events() 
       
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if polygonal_mode:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    
    #desenha_objeto(0.0, 0, 0, 1, 0, 0, -20, 1.5, 1.5, 1.5, 0)
    
    mat_view = view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    glfw.swap_buffers(window)

glfw.terminate()