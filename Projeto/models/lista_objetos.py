from models.objetos import desenha_objeto, load_obj_and_texture

def load_objetos():
    global verticeInicial_abobora, quantosVertices_abobora, textura_abobora
    global verticeInicial_cadeiras, quantosVertices_cadeiras, textura_cadeiras  
    global verticeInicial_camaVelha, quantosVertices_camaVelha, textura_camaVelha
    global verticeInicial_capa1, quantosVertices_capa1, textura_capa1
    global verticeInicial_capa2, quantosVertices_capa2, textura_capa2
    global verticeInicial_capaArrasta, quantosVertices_capaArrasta, textura_capaArrasta
    global verticeInicial_carro, quantosVertices_carro, textura_carro
    global verticeInicial_casa_amarela, quantosVertices_casa_amarela, textura_casa_amarela
    global verticeInicial_casa_simples, quantosVertices_casa_simples, textura_casa_simples
    global verticeInicial_fantasma_puido, quantosVertices_fantasma_puido, textura_fantasma_puido
    global verticeInicial_lanterna, quantosVertices_lanterna, textura_lanterna
    global verticeInicial_mascara_sinistra, quantosVertices_mascara_sinistra, textura_mascara_sinistra
    global verticeInicial_mesa_redonda, quantosVertices_mesa_redonda, textura_mesa_redonda
    global verticeInicial_mesa_retangular, quantosVertices_mesa_retangular, textura_mesa_retangular
    global verticeInicial_sofa_marrom, quantosVertices_sofa_marrom, textura_sofa_marrom
    global verticeInicial_sofa_torto, quantosVertices_sofa_torto, textura_sofa_torto

    verticeInicial_abobora, quantosVertices_abobora, textura_abobora = load_obj_and_texture('objetos/abobora/abobora.obj', ['objetos/abobora/abobora.png'])

    verticeInicial_cadeiras, quantosVertices_cadeiras, textura_cadeiras = load_obj_and_texture('objetos/cadeiras/cadeira.obj', ['objetos/cadeiras/cadeira.png'])

    verticeInicial_camaVelha, quantosVertices_camaVelha, textura_camaVelha = load_obj_and_texture('objetos/cama_velha/cama_velha.obj', ['objetos/cama_velha/cama_velha.png'])

    verticeInicial_capa1, quantosVertices_capa1, textura_capa1 = load_obj_and_texture('objetos/capas/capa1.obj', ['objetos/capas/textura_capas.png'])

    verticeInicial_capa2, quantosVertices_capa2, textura_capa2 = load_obj_and_texture('objetos/capas/capa2.obj', ['objetos/capas/textura_capas.png'])

    verticeInicial_capaArrasta, quantosVertices_capaArrasta, textura_capaArrasta = load_obj_and_texture('objetos/capas/capa_arrasta.obj', ['objetos/capas/textura_capas.png'])

    verticeInicial_carro, quantosVertices_carro, textura_carro = load_obj_and_texture('objetos/carro/carro.obj', ['objetos/carro/carro.png'])

    verticeInicial_casa_amarela, quantosVertices_casa_amarela, textura_casa_amarela = load_obj_and_texture('objetos/casa_amarela/casa_amarela.obj', ['objetos/casa_amarela/casa_amarela.png'])

    verticeInicial_casa_simples, quantosVertices_casa_simples, textura_casa_simples = load_obj_and_texture('objetos/casa_simples/casa.obj', ['objetos/casa_simples/casa.png'])

    verticeInicial_fantasma_puido, quantosVertices_fantasma_puido, textura_fantasma_puido = load_obj_and_texture('objetos/fantasma_puido/fantasma_puido.obj', ['objetos/fantasma_puido/textura_unificada.png'])

    verticeInicial_lanterna, quantosVertices_lanterna, textura_lanterna = load_obj_and_texture('objetos/lanterna/lanterna.obj', ['objetos/lanterna/lanterna.jpg'])

    verticeInicial_mascara_sinistra, quantosVertices_mascara_sinistra, textura_mascara_sinistra = load_obj_and_texture('objetos/mascara_sinistra/mascara_sinistra.obj', ['objetos/mascara_sinistra/mascara_sinistra.jpg'])

    verticeInicial_mesa_redonda, quantosVertices_mesa_redonda, textura_mesa_redonda = load_obj_and_texture('objetos/mesa_redonda/mesa_redonda.obj', ['objetos/mesa_redonda/mesa_redonda.png'])

    verticeInicial_mesa_retangular, quantosVertices_mesa_retangular, textura_mesa_retangular = load_obj_and_texture('objetos/mesa_retangular/mesa_retangular.obj', ['objetos/mesa_retangular/mesa_retangular.png'])

    verticeInicial_sofa_marrom, quantosVertices_sofa_marrom, textura_sofa_marrom = load_obj_and_texture('objetos/sofa_marrom/sofa_marrom.obj', ['objetos/sofa_marrom/sofa_marrom.jpg'])

    verticeInicial_sofa_torto, quantosVertices_sofa_torto, textura_sofa_torto = load_obj_and_texture('objetos/sofa_torto/sofa_torto.obj', ['objetos/sofa_torto/sofa_torto.jpg'])


def desenha_opacos(program, desenha):
    if desenha:
        desenha_objeto(program, verticeInicial_abobora, quantosVertices_abobora,
                       0, #angulo
                       0, 1, 0, #eixo de rotação (x, y, z)
                       0, 0, 0, #translação (x, y, z)
                       0.5, 0.5, 0.5, #escala (x, y, z)
                       textura_abobora[0])
        desenha_objeto(program, verticeInicial_abobora, quantosVertices_abobora,
                0, #angulo
                0, 1, 0, #eixo de rotação (x, y, z)
                0, 0, 0, #translação (x, y, z)
                0.5, 0.5, 0.5, #escala (x, y, z)
                textura_abobora[0])
        
        desenha_objeto(program, verticeInicial_cadeiras, quantosVertices_cadeiras,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    5, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_cadeiras[0])
        
        desenha_objeto(program, verticeInicial_camaVelha, quantosVertices_camaVelha,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    10, 0, 0, #translação (x, y, z)
                    0.001, 0.001, 0.001, #escala (x, y, z)
                    textura_camaVelha[0])   

        desenha_objeto(program, verticeInicial_capa1, quantosVertices_capa1,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    15, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_capa1[0]) 
        
        desenha_objeto(program, verticeInicial_capa2, quantosVertices_capa2,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    20, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_capa2[0])
        
        desenha_objeto(program, verticeInicial_capaArrasta, quantosVertices_capaArrasta,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    25, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_capaArrasta[0])
        
        desenha_objeto(program, verticeInicial_carro, quantosVertices_carro,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    30, 0, 0, #translação (x, y, z)
                    0.001, 0.001, 0.001, #escala (x, y, z)
                    textura_carro[0])
        
        desenha_objeto(program, verticeInicial_casa_amarela, quantosVertices_casa_amarela,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    35, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_casa_amarela[0])
        
        desenha_objeto(program, verticeInicial_casa_simples, quantosVertices_casa_simples,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    40, 0, 0, #translação (x, y, z)
                    0.05, 0.05, 0.05, #escala (x, y, z)
                    textura_casa_simples[0])
        
        desenha_objeto(program, verticeInicial_lanterna, quantosVertices_lanterna,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    50, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_lanterna[0])
        
        desenha_objeto(program, verticeInicial_mascara_sinistra, quantosVertices_mascara_sinistra,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    55, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_mascara_sinistra[0])
        
        desenha_objeto(program, verticeInicial_mesa_redonda, quantosVertices_mesa_redonda,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    60, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_mesa_redonda[0])
        
        desenha_objeto(program, verticeInicial_mesa_retangular, quantosVertices_mesa_retangular,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    65, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_mesa_retangular[0])
        
        desenha_objeto(program, verticeInicial_sofa_marrom, quantosVertices_sofa_marrom,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    46, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_sofa_marrom[0])
        
        desenha_objeto(program, verticeInicial_sofa_torto, quantosVertices_sofa_torto,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    75, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_sofa_torto[0])   
    
def desenha_transparentes(program, desenha):
    if desenha:
        desenha_objeto(program, verticeInicial_fantasma_puido, quantosVertices_fantasma_puido,
                    0, #angulo
                    0, 1, 0, #eixo de rotação (x, y, z)
                    45, 0, 0, #translação (x, y, z)
                    0.5, 0.5, 0.5, #escala (x, y, z)
                    textura_fantasma_puido[0])