from OpenGL.GL import *
import glfw
from graficos.shader_s import Shader

def create_window(largura, altura):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    # 🔥 ADICIONAR ISSO
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

    altura = 700
    largura = 700

    window = glfw.create_window(largura, altura, "O Assombro", None, None)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        
    glfw.make_context_current(window)

    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)

    return window