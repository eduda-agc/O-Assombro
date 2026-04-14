from OpenGL.GL import *
import glfw
from graficos.shader_s import Shader

def create_window(largura, altura):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    altura = 700
    largura = 700

    window = glfw.create_window(largura, altura, "O Assombro", None, None)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        
    glfw.make_context_current(window)

    glEnable(GL_TEXTURE_2D)
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glEnable( GL_BLEND )
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
    glEnable(GL_LINE_SMOOTH)
    return window