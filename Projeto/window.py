
import glfw
from OpenGL.GL import *

from Projeto.shader_s import Shader

def init_window(altura, largura):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    window = glfw.create_window(largura, altura, "O Assombro", None, None)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        
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

    return window, program