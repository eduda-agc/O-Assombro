import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
from numpy import random
from PIL import Image

from Projeto.shader_s import Shader

from Projeto.loader import *
from Projeto.texture import *
from Projeto.utils import *

# inicializando a janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

altura = 700
largura = 700

window = glfw.create_window(largura, altura, "Programa", None, None)

if (window == None):
    print("Failed to create GLFW window")
    glfwTerminate()
    
glfw.make_context_current(window)

# criando o shader
ourShader = Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
ourShader.use()

program = ourShader.getProgram()

# carregando modelos a partir de arquivos .obj e texturas a partir de arquivos .jpg 
glEnable(GL_TEXTURE_2D)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
glEnable(GL_LINE_SMOOTH)

# carrega modelo abobora
vi_abobora, quantosV_abobora = load_obj_and_texture("objetos/abobora/abobora.obj", ["objetos/abobora/texturas/..."])

def desenha_abobora(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, textureId):

    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
           
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, textureId)
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, vi_abobora, quantosV_abobora) ## renderizando