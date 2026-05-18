from models.objetos import desenha_objeto as desenha_objeto_base, load_obj_and_texture
import random
import numpy as np

########################################################
# PARAMETROS DE ILUMINACAO DOS OBJETOS
########################################################

MATERIAL_DEFAULT = {
    "diffuse": 1.0,
    "specular": 0.25,
    "receive_candles": False
}

MATERIAIS = {
    "abobora": {"diffuse": 1.15, "specular": 0.18, "receive_candles": False},
    "cadeiras": {"diffuse": 0.95, "specular": 0.22, "receive_candles": True},
    "cama": {"diffuse": 0.90, "specular": 0.12, "receive_candles": True},
    "carro": {"diffuse": 0.85, "specular": 0.70, "receive_candles": False},
    "casa": {"diffuse": 0.95, "specular": 0.16, "receive_candles": False},
    "fantasma": {"diffuse": 0.70, "specular": 0.45, "receive_candles": True},
    "garota": {"diffuse": 0.80, "specular": 0.20, "receive_candles": True},
    "lampada_mao": {"diffuse": 0.90, "specular": 0.55, "receive_candles": False},
    "lua": {"diffuse": 1.10, "specular": 0.05, "receive_candles": False},
    "mascara": {"diffuse": 0.85, "specular": 0.60, "receive_candles": False},
    "mesa_redonda": {"diffuse": 0.95, "specular": 0.28, "receive_candles": True},
    "mesa_retangular": {"diffuse": 0.95, "specular": 0.30, "receive_candles": True},
    "sofa": {"diffuse": 0.85, "specular": 0.10, "receive_candles": True},
    "vela": {"diffuse": 1.05, "specular": 0.18, "receive_candles": True},
    "chao": {"diffuse": 0.90, "specular": 0.08, "receive_candles": False},
    "arvore": {"diffuse": 0.85, "specular": 0.06, "receive_candles": False},
    "ceu": {"diffuse": 0.65, "specular": 0.00, "receive_candles": False}
}

materiais_por_vertice = {}

def desenha_objeto(
    program,
    verticeInicial,
    quantosVertices,
    angle,
    r_x,
    r_y,
    r_z,
    t_x,
    t_y,
    t_z,
    s_x,
    s_y,
    s_z,
    textureId
):

    material = materiais_por_vertice.get(
        verticeInicial,
        MATERIAL_DEFAULT
    )

    desenha_objeto_base(
        program,
        verticeInicial,
        quantosVertices,
        angle,
        r_x,
        r_y,
        r_z,
        t_x,
        t_y,
        t_z,
        s_x,
        s_y,
        s_z,
        textureId,
        material["diffuse"],
        material["specular"],
        material["receive_candles"]
    )

########################################################
# POSIÇÕES / CONTROLES
########################################################

cadeira1_pos = [16, -4.5, -5]

cadeira2_rot = -90

garota_rot_y = 0
garota_pos = [14, -4.2, -6]
garota_scale = 0.000

mesa_posicao = [17, -5.5, -5]

fantasma_scale = 0.5

abobora_angle = 0

carro_pos = [4, -4.75, 2]

########################################################
# POSIÇÕES DAS VELAS
########################################################

velas_pos = [
    [13.25, -1.0, -5.0],
    [13.28, -1.0, -8.0],
    [15.0, -1.0, -11.0],
    [18.0, -1.0, -11.0]
]

########################################################
# OBJETOS INTERNOS DA CASA
########################################################

def desenha_objetos_internos(program):

    ####################################################
    # CADEIRAS
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_cadeiras,
        quantosVertices_cadeiras,
        0,
        0, 1, 0,
        cadeira1_pos[0],
        cadeira1_pos[1],
        cadeira1_pos[2],
        0.5, 0.5, 0.5,
        textura_cadeiras[0]
    )

    desenha_objeto(
        program,
        verticeInicial_cadeiras,
        quantosVertices_cadeiras,
        90,
        1, 0, 0,
        16, -4, -3.5,
        0.5, 0.5, 0.5,
        textura_cadeiras[0]
    )

    desenha_objeto(
        program,
        verticeInicial_cadeiras,
        quantosVertices_cadeiras,
        cadeira2_rot,
        0, 1, 0,
        17, -4.2, -6.5,
        0.5, 0.5, 0.5,
        textura_cadeiras[0]
    )

    ####################################################
    # CAMA
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_camaVelha,
        quantosVertices_camaVelha,
        -90,
        0, 1, 0,
        14, -4.2, -10,
        0.01, 0.01, 0.01,
        textura_camaVelha[0]
    )

    ####################################################
    # GAROTA JUMPSCARE
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_garota_horror,
        quantosVertices_garota_horror,
        garota_rot_y,
        0, 1, 0,
        garota_pos[0],
        garota_pos[1],
        garota_pos[2],
        garota_scale,
        garota_scale,
        garota_scale,
        textura_garota_horror[0]
    )

    ####################################################
    # MESA REDONDA
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_mesa_redonda,
        quantosVertices_mesa_redonda,
        0,
        0, 1, 0,
        14, -1.2, -1.7,
        0.2, 0.2, 0.2,
        textura_mesa_redonda[0]
    )

    ####################################################
    # MESA RETANGULAR
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_mesa_retangular,
        quantosVertices_mesa_retangular,
        0,
        0, 1, 0,
        mesa_posicao[0],
        mesa_posicao[1],
        mesa_posicao[2],
        0.45, 0.45, 0.45,
        textura_mesa_retangular[0]
    )

    ####################################################
    # SOFÁ
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_sofa_marrom,
        quantosVertices_sofa_marrom,
        0,
        0, 1, 0,
        17, -4.2, -10.1,
        0.8, 0.8, 0.8,
        textura_sofa_marrom[0]
    )

########################################################
# OBJETOS EXTERNOS / GERAIS
########################################################

def desenha_opacos(program, desenha):

    if not desenha:
        return

    ####################################################
    # ABÓBORA
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_abobora,
        quantosVertices_abobora,
        abobora_angle,
        0, 1, 0,
        8, -4.8, 0,
        0.5, 0.5, 0.5,
        textura_abobora[0]
    )

    ####################################################
    # CARRO
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_carro,
        quantosVertices_carro,
        180,
        0, 1, 0,
        carro_pos[0],
        carro_pos[1],
        carro_pos[2],
        0.007, 0.007, 0.007,
        textura_carro[0]
    )

    ####################################################
    # CASA
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_casa_amarela,
        quantosVertices_casa_amarela,
        0,
        0, 1, 0,
        13, -4.2, 0,
        0.8, 0.8, 0.8,
        textura_casa_amarela[0]
    )

    ####################################################
    # LUA
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_lua,
        quantosVertices_lua,
        0,
        0, 1, 0,
        36, 20, 0,
        0.1, 0.1, 0.1,
        textura_lua[0]
    )

    ####################################################
    # MÁSCARA
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_mascara_sinistra,
        quantosVertices_mascara_sinistra,
        0,
        0, 1, 0,
        15, -5, -1.10,
        0.5, 0.5, 0.5,
        textura_mascara_sinistra[0]
    )

    ####################################################
    # VELAS
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_vela_parede,
        quantosVertices_vela_parede,
        80,
        0, 1, 0,
        13.25, -1.5, -5,
        0.02, 0.02, 0.02,
        textura_vela_parede[0]
    )

    desenha_objeto(
        program,
        verticeInicial_vela_parede,
        quantosVertices_vela_parede,
        80,
        0, 1, 0,
        13.28, -1.5, -8,
        0.02, 0.02, 0.02,
        textura_vela_parede[0]
    )

    desenha_objeto(
        program,
        verticeInicial_vela_parede,
        quantosVertices_vela_parede,
        -10,
        0, 1, 0,
        15, -1.5, -11,
        0.02, 0.02, 0.02,
        textura_vela_parede[0]
    )

    desenha_objeto(
        program,
        verticeInicial_vela_parede,
        quantosVertices_vela_parede,
        -10,
        0, 1, 0,
        18, -1.5, -11,
        0.02, 0.02, 0.02,
        textura_vela_parede[0]
    )

    ####################################################
    # CHÃO
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_chao,
        quantosVertices_chao,
        0,
        0, 1, 0,
        0, -5, 0,
        2, 2, 2,
        textura_chao[0]
    )

    ####################################################
    # CÉU
    ####################################################

    desenha_objeto(
        program,
        verticeInicial_ceu,
        quantosVertices_ceu,
        0,
        0, 0, 0,
        0, 0, 0,
        45, 45, 45,
        textura_ceu[0]
    )

########################################################
# ÁRVORES
########################################################

def desenha_arvores(program, desenha, posicoes_arvores):

    if not desenha:
        return

    for pos in posicoes_arvores:

        x, z = pos

        desenha_objeto(
            program,
            verticeInicial_arvore,
            quantosVertices_arvore,
            0,
            0, 1, 0,
            x, -5, z,
            0.5, 0.5, 0.5,
            textura_arvore[0]
        )

########################################################
# TRANSPARENTES
########################################################

def desenha_transparentes(program, desenha):

    if not desenha:
        return

    desenha_objeto(
        program,
        verticeInicial_fantasma_puido,
        quantosVertices_fantasma_puido,
        -150,
        0, 1, 0,
        18, -1, -5,
        fantasma_scale,
        fantasma_scale,
        fantasma_scale,
        textura_fantasma_puido[0]
    )

########################################################
# ITEM NA MÃO
########################################################

def desenha_item_mao(
    program,
    verticeInicial,
    quantosVertices,
    textura
):
    import camera.controls as controls
    import glm

    right = glm.normalize(
        glm.cross(
            controls.cameraFront,
            controls.cameraUp
        )
    )

    offset_frente = 0.5
    offset_direita = 0.3
    offset_cima = -0.2

    pos = (
        controls.cameraPos
        + controls.cameraFront * offset_frente
        + right * offset_direita
        + controls.cameraUp * offset_cima
    )

    pos += controls.headbob_offset * 0.5

    desenha_objeto(
        program,
        verticeInicial,
        quantosVertices,
        0,
        0, 1, 0,
        pos.x,
        pos.y,
        pos.z,
        0.05,
        0.05,
        0.05,
        textura
    )

########################################################
# LOAD OBJETOS
########################################################

def load_objetos():

    global verticeInicial_abobora
    global quantosVertices_abobora
    global textura_abobora

    global verticeInicial_cadeiras
    global quantosVertices_cadeiras
    global textura_cadeiras

    global verticeInicial_camaVelha
    global quantosVertices_camaVelha
    global textura_camaVelha

    global verticeInicial_carro
    global quantosVertices_carro
    global textura_carro

    global verticeInicial_casa_amarela
    global quantosVertices_casa_amarela
    global textura_casa_amarela

    global verticeInicial_fantasma_puido
    global quantosVertices_fantasma_puido
    global textura_fantasma_puido

    global verticeInicial_garota_horror
    global quantosVertices_garota_horror
    global textura_garota_horror

    global verticeInicial_lampada_mao
    global quantosVertices_lampada_mao
    global textura_lampada_mao

    global verticeInicial_lua
    global quantosVertices_lua
    global textura_lua

    global verticeInicial_mascara_sinistra
    global quantosVertices_mascara_sinistra
    global textura_mascara_sinistra

    global verticeInicial_mesa_redonda
    global quantosVertices_mesa_redonda
    global textura_mesa_redonda

    global verticeInicial_mesa_retangular
    global quantosVertices_mesa_retangular
    global textura_mesa_retangular

    global verticeInicial_sofa_marrom
    global quantosVertices_sofa_marrom
    global textura_sofa_marrom

    global verticeInicial_vela_parede
    global quantosVertices_vela_parede
    global textura_vela_parede

    global verticeInicial_chao
    global quantosVertices_chao
    global textura_chao

    global verticeInicial_arvore
    global quantosVertices_arvore
    global textura_arvore

    global verticeInicial_ceu
    global quantosVertices_ceu
    global textura_ceu

    ####################################################
    # LOADS
    ####################################################

    verticeInicial_abobora, quantosVertices_abobora, textura_abobora = load_obj_and_texture(
        'objetos/abobora/abobora.obj',
        ['objetos/abobora/abobora.png']
    )

    verticeInicial_cadeiras, quantosVertices_cadeiras, textura_cadeiras = load_obj_and_texture(
        'objetos/cadeiras/cadeira.obj',
        ['objetos/cadeiras/cadeira.png']
    )

    verticeInicial_camaVelha, quantosVertices_camaVelha, textura_camaVelha = load_obj_and_texture(
        'objetos/cama_velha/cama_velha.obj',
        ['objetos/cama_velha/cama_velha.png']
    )

    verticeInicial_carro, quantosVertices_carro, textura_carro = load_obj_and_texture(
        'objetos/carro/carro.obj',
        ['objetos/carro/carro.png']
    )

    verticeInicial_casa_amarela, quantosVertices_casa_amarela, textura_casa_amarela = load_obj_and_texture(
        'objetos/casa_amarela/casa_amarela.obj',
        ['objetos/casa_amarela/casa_amarela.png']
    )

    verticeInicial_fantasma_puido, quantosVertices_fantasma_puido, textura_fantasma_puido = load_obj_and_texture(
        'objetos/fantasma_puido/fantasma_puido.obj',
        ['objetos/fantasma_puido/textura_unificada.png']
    )

    verticeInicial_garota_horror, quantosVertices_garota_horror, textura_garota_horror = load_obj_and_texture(
        'objetos/garota_horror/garota_horror.obj',
        ['objetos/garota_horror/textura_unificada.png']
    )

    verticeInicial_lampada_mao, quantosVertices_lampada_mao, textura_lampada_mao = load_obj_and_texture(
        'objetos/lampada_mao/lampada_mao.obj',
        ['objetos/lampada_mao/lampada_mao.png']
    )

    verticeInicial_lua, quantosVertices_lua, textura_lua = load_obj_and_texture(
        'objetos/lua/lua.obj',
        ['objetos/lua/lua.png']
    )

    verticeInicial_mascara_sinistra, quantosVertices_mascara_sinistra, textura_mascara_sinistra = load_obj_and_texture(
        'objetos/mascara_sinistra/mascara_sinistra.obj',
        ['objetos/mascara_sinistra/mascara_sinistra.jpg']
    )

    verticeInicial_mesa_redonda, quantosVertices_mesa_redonda, textura_mesa_redonda = load_obj_and_texture(
        'objetos/mesa_redonda/mesa_redonda.obj',
        ['objetos/mesa_redonda/mesa_redonda.png']
    )

    verticeInicial_mesa_retangular, quantosVertices_mesa_retangular, textura_mesa_retangular = load_obj_and_texture(
        'objetos/mesa_retangular/mesa_retangular.obj',
        ['objetos/mesa_retangular/mesa_retangular.png']
    )

    verticeInicial_sofa_marrom, quantosVertices_sofa_marrom, textura_sofa_marrom = load_obj_and_texture(
        'objetos/sofa_marrom/sofa_marrom.obj',
        ['objetos/sofa_marrom/sofa_marrom.jpg']
    )

    verticeInicial_vela_parede, quantosVertices_vela_parede, textura_vela_parede = load_obj_and_texture(
        'objetos/vela_parede/vela_parede.obj',
        ['objetos/vela_parede/textura_unificada.png']
    )

    verticeInicial_chao, quantosVertices_chao, textura_chao = load_obj_and_texture(
        'objetos/ambiente/chao/chao.obj',
        ['objetos/ambiente/chao/chao.jpg']
    )

    verticeInicial_arvore, quantosVertices_arvore, textura_arvore = load_obj_and_texture(
        'objetos/ambiente/arvores/arvore.obj',
        ['objetos/ambiente/arvores/arvore.png']
    )

    verticeInicial_ceu, quantosVertices_ceu, textura_ceu = load_obj_and_texture(
        'objetos/ambiente/ceu/ceu.obj',
        ['objetos/ambiente/ceu/ceu.png']
    )

    materiais_por_vertice.clear()
    materiais_por_vertice.update({
        verticeInicial_abobora: MATERIAIS["abobora"],
        verticeInicial_cadeiras: MATERIAIS["cadeiras"],
        verticeInicial_camaVelha: MATERIAIS["cama"],
        verticeInicial_carro: MATERIAIS["carro"],
        verticeInicial_casa_amarela: MATERIAIS["casa"],
        verticeInicial_fantasma_puido: MATERIAIS["fantasma"],
        verticeInicial_garota_horror: MATERIAIS["garota"],
        verticeInicial_lampada_mao: MATERIAIS["lampada_mao"],
        verticeInicial_lua: MATERIAIS["lua"],
        verticeInicial_mascara_sinistra: MATERIAIS["mascara"],
        verticeInicial_mesa_redonda: MATERIAIS["mesa_redonda"],
        verticeInicial_mesa_retangular: MATERIAIS["mesa_retangular"],
        verticeInicial_sofa_marrom: MATERIAIS["sofa"],
        verticeInicial_vela_parede: MATERIAIS["vela"],
        verticeInicial_chao: MATERIAIS["chao"],
        verticeInicial_arvore: MATERIAIS["arvore"],
        verticeInicial_ceu: MATERIAIS["ceu"]
    })
