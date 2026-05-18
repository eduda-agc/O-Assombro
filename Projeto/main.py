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
MARGEM = 10
QTD_ARVORES = 100

############################################################
# JANELA
############################################################

window = create_window(LARGURA, ALTURA)

############################################################
# SHADER
############################################################

ourShader = Shader(
    "graficos/shaders/vertex_shader.vs",
    "graficos/shaders/fragment_shader.fs"
)

ourShader.use()

program = ourShader.getProgram()

############################################################
# UNIFORMS
############################################################

loc_useLighting = glGetUniformLocation(
    program,
    "useLighting"
)

############################################################
# CARREGA OBJETOS
############################################################

objs.load_objetos()

############################################################
# VAO
############################################################

VAO = glGenVertexArrays(1)

glBindVertexArray(VAO)

############################################################
# BUFFERS
############################################################

buffer = setup_buffers(
    vertices_list,
    textures_coord_list,
    normals_list,
    program
)

############################################################
# CALLBACK RESIZE
############################################################

def framebuffer_size_callback(window, largura, altura):

    glViewport(
        0,
        0,
        largura,
        altura
    )

############################################################
# INPUTS
############################################################

glfw.set_key_callback(
    window,
    key_event
)

glfw.set_framebuffer_size_callback(
    window,
    framebuffer_size_callback
)

glfw.set_cursor_pos_callback(
    window,
    mouse_callback
)

glfw.set_scroll_callback(
    window,
    scroll_callback
)

############################################################
# MOUSE
############################################################

glfw.set_input_mode(
    window,
    glfw.CURSOR,
    glfw.CURSOR_DISABLED
)

############################################################
# CAMERA
############################################################

init_camera(
    LARGURA,
    ALTURA
)

############################################################
# MOSTRA JANELA
############################################################

glfw.show_window(window)

############################################################
# OPENGL CONFIG
############################################################

glEnable(GL_DEPTH_TEST)

glEnable(GL_BLEND)

glBlendFunc(
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA
)

glUniform1i(
    glGetUniformLocation(program, "imagem"),
    0
)

############################################################
# CASA
############################################################

CASA_X_MIN = 10
CASA_X_MAX = 21

CASA_Z_MIN = -13
CASA_Z_MAX = 0

############################################################
# FUNÇÃO CASA
############################################################

def dentro_da_casa(x, z):

    return (
        CASA_X_MIN <= x <= CASA_X_MAX
        and
        CASA_Z_MIN <= z <= CASA_Z_MAX
    )

############################################################
# ÁRVORES
############################################################

posicoes_arvores = []

while len(posicoes_arvores) < QTD_ARVORES:

    x = random.uniform(
        -TAM_CHAO + MARGEM,
        TAM_CHAO - MARGEM
    )

    z = random.uniform(
        -TAM_CHAO + MARGEM,
        TAM_CHAO - MARGEM
    )

    if (
        CASA_X_MIN - MARGEM <= x <= CASA_X_MAX + MARGEM
        and
        CASA_Z_MIN - MARGEM <= z <= CASA_Z_MAX + MARGEM
    ):
        continue

    if not dentro_da_casa(x, z):

        posicoes_arvores.append((x, z))

############################################################
# JUMPSCARE
############################################################

jumpscare_ativo = False
jumpscare_iniciado = False

tempo_jumpscare = 0

############################################################
# TRIGGER
############################################################

def trigger_jumpscare():

    pos = controls.cameraPos

    return (
        14 < pos.x < 16.5
        and
        -9 < pos.z < -3
    )

############################################################
# LOOP PRINCIPAL
############################################################

while not glfw.window_should_close(window):

    ########################################################
    # TEMPO
    ########################################################

    currentFrame = glfw.get_time()

    controls.deltaTime = (
        currentFrame - controls.lastFrame
    )

    controls.lastFrame = currentFrame

    controls.update_headbob()

    ########################################################
    # EVENTOS
    ########################################################

    glfw.poll_events()

    ########################################################
    # LIMPA TELA
    ########################################################

    glClearColor(
        0.02,
        0.02,
        0.02,
        1.0
    )

    glClear(
        GL_COLOR_BUFFER_BIT
        |
        GL_DEPTH_BUFFER_BIT
    )

    ########################################################
    # POLYGON MODE
    ########################################################

    if controls.polygonal_mode:

        glPolygonMode(
            GL_FRONT_AND_BACK,
            GL_LINE
        )

    else:

        glPolygonMode(
            GL_FRONT_AND_BACK,
            GL_FILL
        )

    ########################################################
    # TEXTURA
    ########################################################

    glActiveTexture(GL_TEXTURE0)

    ########################################################
    # VIEW / PROJECTION
    ########################################################

    mat_view = view()

    loc_view = glGetUniformLocation(
        program,
        "view"
    )

    glUniformMatrix4fv(
        loc_view,
        1,
        GL_TRUE,
        mat_view
    )

    mat_projection = projection(
        ALTURA,
        LARGURA
    )

    loc_projection = glGetUniformLocation(
        program,
        "projection"
    )

    glUniformMatrix4fv(
        loc_projection,
        1,
        GL_TRUE,
        mat_projection
    )

    glUniform1f(
    glGetUniformLocation(program, "time"),
    glfw.get_time()
    )

    ########################################################
    # LUZ 0 = LANTERNA
    ########################################################

    right = glm.normalize(
        glm.cross(
            controls.cameraFront,
            controls.cameraUp
        )
    )

    lightPos_mao = (
        controls.cameraPos
        + controls.cameraFront * 0.6
        + right * 0.25
        - controls.cameraUp * 0.15
    )

    lightDir_mao = controls.cameraFront

    ########################################################
    # LUZES 1 E 2 = FARÓIS
    ########################################################

    carro_pos = glm.vec3(
        objs.carro_pos[0],
        objs.carro_pos[1],
        objs.carro_pos[2]
    )

    farol_esquerdo = (
        carro_pos
        + glm.vec3(-0.6, 0.4, 0)
    )

    farol_direito = (
        carro_pos
        + glm.vec3(0.6, 0.4, 0)
    )

    farol_dir = glm.vec3(
        0.0,
        0.0,
        -1.0
    )

    ########################################################
    # LUZES 3-6 = VELAS
    ########################################################

    velas_pos = [
        glm.vec3(13.25, -1.2, -5.0),
        glm.vec3(13.28, -1.2, -8.0),
        glm.vec3(15.0, -1.2, -11.0),
        glm.vec3(18.0, -1.2, -11.0)
    ]

    ########################################################
    # POSIÇÕES
    ########################################################

    glUniform3f(
        glGetUniformLocation(program, "lightPos[0]"),
        lightPos_mao.x,
        lightPos_mao.y,
        lightPos_mao.z
    )

    glUniform3f(
        glGetUniformLocation(program, "lightPos[1]"),
        farol_esquerdo.x,
        farol_esquerdo.y,
        farol_esquerdo.z
    )

    glUniform3f(
        glGetUniformLocation(program, "lightPos[2]"),
        farol_direito.x,
        farol_direito.y,
        farol_direito.z
    )

    for i in range(4):

        glUniform3f(
            glGetUniformLocation(program, f"lightPos[{i + 3}]"),
            velas_pos[i].x,
            velas_pos[i].y,
            velas_pos[i].z
        )

    ########################################################
    # DIREÇÕES
    ########################################################

    glUniform3f(
        glGetUniformLocation(program, "lightDir[0]"),
        lightDir_mao.x,
        lightDir_mao.y,
        lightDir_mao.z
    )

    glUniform3f(
        glGetUniformLocation(program, "lightDir[1]"),
        farol_dir.x,
        farol_dir.y,
        farol_dir.z
    )

    glUniform3f(
        glGetUniformLocation(program, "lightDir[2]"),
        farol_dir.x,
        farol_dir.y,
        farol_dir.z
    )

    ########################################################
    # DIREÇÕES DAS VELAS
    ########################################################

    for i in range(4):

        glUniform3f(
            glGetUniformLocation(program, f"lightDir[{i + 3}]"),
            0.0,
            -1.0,
            0.0
        )

    ########################################################
    # CORES
    ########################################################

    cor_lanterna = (
        1.0 * controls.lanterna_mao_intensidade,
        0.95 * controls.lanterna_mao_intensidade,
        0.85 * controls.lanterna_mao_intensidade
    ) if controls.lanterna_mao_ligada else (
        0.0,
        0.0,
        0.0
    )

    cor_farois = (
        1.0,
        1.0,
        0.9
    ) if controls.farois_carro_ligados else (
        0.0,
        0.0,
        0.0
    )

    cor_velas_ligadas = (
        1.0,
        1.0,
        1.0
    ) if controls.velas_luz_branca else (
        1.0,
        0.55,
        0.15
    )

    cor_velas = cor_velas_ligadas if controls.velas_ligadas else (
        0.0,
        0.0,
        0.0
    )

    glUniform3f(glGetUniformLocation(program, "candleMin"),
    8.0, -6.0, -13.0)

    glUniform3f(glGetUniformLocation(program, "candleMax"),
    21.0, -1.2, -2.3)

    # lanterna
    glUniform3f(
        glGetUniformLocation(program, "lightColor[0]"),
        cor_lanterna[0],
        cor_lanterna[1],
        cor_lanterna[2]
    )

    # farol esquerdo
    glUniform3f(
        glGetUniformLocation(program, "lightColor[1]"),
        cor_farois[0],
        cor_farois[1],
        cor_farois[2]
    )

    # farol direito
    glUniform3f(
        glGetUniformLocation(program, "lightColor[2]"),
        cor_farois[0],
        cor_farois[1],
        cor_farois[2]
    )

    ########################################################
    # CORES DAS VELAS
    ########################################################

    for i in range(4):

        glUniform3f(
            glGetUniformLocation(program, f"lightColor[{i + 3}]"),
            cor_velas[0],
            cor_velas[1],
            cor_velas[2]
        )

    ########################################################
    # JUMPSCARE
    ########################################################

    if trigger_jumpscare() and not jumpscare_iniciado:

        jumpscare_ativo = True
        jumpscare_iniciado = True

        tempo_jumpscare = glfw.get_time()

    if jumpscare_ativo:

        tempo = glfw.get_time() - tempo_jumpscare

        dx = (
            controls.cameraPos.x
            -
            objs.garota_pos[0]
        )

        dz = (
            controls.cameraPos.z
            -
            objs.garota_pos[2]
        )

        objs.garota_rot_y = (
            math.degrees(math.atan2(dx, dz))
            + 90
        )

        objs.garota_scale = 0.009

        distancia = 1.0

        alvo = (
            controls.cameraPos
            +
            controls.cameraFront * distancia
        )

        direcao = (
            alvo
            -
            glm.vec3(*objs.garota_pos)
        )

        if glm.length(direcao) > 0.01:

            direcao = glm.normalize(direcao)

            objs.garota_pos[0] += direcao.x * 0.2
            objs.garota_pos[2] += direcao.z * 0.2

        if tempo > 3:

            jumpscare_ativo = False
            jumpscare_iniciado = False

            objs.garota_scale = 0

            objs.garota_pos = [
                14,
                -4.2,
                -6
            ]

    ########################################################
    # OBJETOS ILUMINADOS
    ########################################################

    glUniform1i(
        loc_useLighting,
        True
    )

    ########################################################
    # OBJETOS INTERNOS
    ########################################################

    objs.desenha_objetos_internos(
        program
    )

    ########################################################
    # OBJETOS EXTERNOS
    ########################################################

    objs.desenha_opacos(
        program,
        True
    )

    ########################################################
    # ÁRVORES
    ########################################################

    objs.desenha_arvores(
        program,
        True,
        posicoes_arvores
    )

    ########################################################
    # TRANSPARENTES
    ########################################################

    objs.desenha_transparentes(
        program,
        True
    )

    ########################################################
    # ITEM NA MÃO
    ########################################################

    glDisable(GL_DEPTH_TEST)

    glUniform1i(
        loc_useLighting,
        False
    )

    objs.desenha_item_mao(
        program,
        objs.verticeInicial_lampada_mao,
        objs.quantosVertices_lampada_mao,
        objs.textura_lampada_mao[0]
    )

    glEnable(GL_DEPTH_TEST)

    ########################################################
    # SWAP
    ########################################################

    glfw.swap_buffers(window)

############################################################
# FINALIZA
############################################################

glfw.terminate()
