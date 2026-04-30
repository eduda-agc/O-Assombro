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
import models.lista_objetos as objs


from transformacoes_mat.transforms import *

ALTURA = 700
LARGURA = 700   
TAM_CHAO = 40 
MARGEM = 2 #margem para não desenhar objetos muito próximos do limite do chão
QTD_ARVORES = 20



window = create_window(LARGURA, ALTURA)

ourShader = Shader("graficos/shaders/vertex_shader.vs", "graficos/shaders/fragment_shader.fs")
ourShader.use()



program = ourShader.getProgram()

objs.load_objetos()  

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


CASA_X_MIN = 5
CASA_X_MAX = 20
CASA_Z_MIN = 3
CASA_Z_MAX = -20

def dentro_da_casa(x, z):
    return ((CASA_X_MIN <= x <= CASA_X_MAX) and
            (CASA_Z_MIN <= z <= CASA_Z_MAX))



#definir posições das árvores
posicoes_arvores = []

while len(posicoes_arvores) < QTD_ARVORES:
    x = random.uniform(-TAM_CHAO + MARGEM, TAM_CHAO - MARGEM)
    z = random.uniform(-TAM_CHAO + MARGEM, TAM_CHAO - MARGEM)

    if not dentro_da_casa(x, z):
        print(f"Adicionando árvore na posição ({x:.2f}, {z:.2f})")
        posicoes_arvores.append((x, z))


jumpscare_ativo = False
jumpscare_iniciado = False
tempo_jumpscare = 0

def trigger_jumpscare():
    pos = controls.cameraPos
    return (14 < pos.x < 16.5 and -9 < pos.z < -3)

while not glfw.window_should_close(window):

    currentFrame = glfw.get_time()
    controls.deltaTime = currentFrame - controls.lastFrame
    controls.lastFrame = currentFrame
    controls.update_headbob()

    glfw.poll_events() 
       
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glClearColor(0.0, 0.0, 0.1, 1.0) #cor do ceu
    
    if controls.polygonal_mode:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    glActiveTexture(GL_TEXTURE0)

    if trigger_jumpscare() and not jumpscare_iniciado:
        jumpscare_ativo = True
        jumpscare_iniciado = True
        tempo_jumpscare = glfw.get_time()

    if jumpscare_ativo:
        tempo = glfw.get_time() - tempo_jumpscare

        dx = controls.cameraPos.x - objs.garota_pos[0]
        dz = controls.cameraPos.z - objs.garota_pos[2]

        objs.garota_rot_y = math.degrees(math.atan2(dx, dz)) + 90  

        # aumenta escala rapidamente
        objs.garota_scale = 0.009

        distancia = 1.0

        # posição alvo (1 unidade à frente da câmera)
        alvo = controls.cameraPos + controls.cameraFront * distancia

        # direção até o alvo
        direcao = alvo - glm.vec3(*objs.garota_pos)

        # suavização (movimento progressivo)
        if glm.length(direcao) > 0.01:
            direcao = glm.normalize(direcao)
            
            objs.garota_pos[0] += direcao.x * 0.2
            objs.garota_pos[2] += direcao.z * 0.2

        if tempo > 3: # depois de 1.5 segundos, desativa o jumpscare
            jumpscare_ativo = False
            jumpscare_iniciado = False
            objs.garota_scale = 0
            objs.garota_pos = [14, -4.2, -6]

    objs.desenha_opacos(program, True) 
    objs.desenha_arvores(program, True, posicoes_arvores)
    objs.desenha_transparentes(program, True)

    #mat = transformacoes();

    mat_view = view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    

    mat_projection = projection(ALTURA, LARGURA)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    objs.desenha_opacos(program, True)
    objs.desenha_arvores(program, True, posicoes_arvores)
    objs.desenha_transparentes(program, True)  

    #objeto na mao
    glDisable(GL_DEPTH_TEST)
    objs.desenha_item_mao(
        program,
        objs.verticeInicial_lampada_mao,   
        objs.quantosVertices_lampada_mao,
        objs.textura_lampada_mao[0]
    )

    glEnable(GL_DEPTH_TEST)
    
    glfw.swap_buffers(window)

glfw.terminate()