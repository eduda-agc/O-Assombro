from models.objetos import desenha_objeto, load_obj_and_texture

def load_objetos():
    global verticeInicial_casa, quantosVertices_casa, textura_casa
    global verticeInicial_camaVelha, quantosVertices_camaVelha, textura_camaVelha
    global verticeInicial_abobora, quantosVertices_abobora, textura_abobora
    global verticeInicial_capa2, quantosVertices_capa2, textura_capa2
    global verticeInicial_capaArrasta, quantosVertices_capaArrasta, textura_capaArrasta
    global verticeInicial_fantasma_puido, quantosVertices_fantasma_puido, textura_fantasma_puido

    verticeInicial_casa, quantosVertices_casa, textura_casa = load_obj_and_texture(
        'objetos/casa_simples/casa.obj', ['objetos/casa_simples/casa.png']
    )

    verticeInicial_camaVelha, quantosVertices_camaVelha, textura_camaVelha = load_obj_and_texture(
        'objetos/cama_velha/cama_velha.obj', ['objetos/cama_velha/cama_velha.png']
    )

    verticeInicial_abobora, quantosVertices_abobora, textura_abobora = load_obj_and_texture(
        'objetos/abobora/abobora.obj', ['objetos/abobora/abobora.png']
    )

    verticeInicial_capa2, quantosVertices_capa2, textura_capa2 = load_obj_and_texture(
        'objetos/capas/capa2.obj', ['objetos/capas/textura_capas.png']
    )

    verticeInicial_capaArrasta, quantosVertices_capaArrasta, textura_capaArrasta = load_obj_and_texture(
        'objetos/capas/capaArrasta.obj', ['objetos/capas/textura_capas.png']
    )

    verticeInicial_fantasma_puido, quantosVertices_fantasma_puido, textura_fantasma_puido = load_obj_and_texture(
        'objetos/fantasma_puido/fantasma_puido.obj', ['objetos/fantasma_puido/textura_unificada.png']
    )   

def desenha_objetos(program):
    desenha_objeto(program, verticeInicial_casa, quantosVertices_casa,
               0, #angulo
               0, 1, 0, #eixo de rotação (x, y, z)
               0, 0, 0, #translação (x, y, z)
               0.5, 0.5, 0.5, #escala (x, y, z)
               textura_casa[0])
    
    # a cama velha está dentro da casa
    desenha_objeto(program, verticeInicial_camaVelha, quantosVertices_camaVelha, 
                0, #angulo
                0, 1, 0, #eixo de rotação (x, y, z)
                5, 0, 0, #translação (x, y, z)
                0.01, 0.01, 0.01, #escala (x, y, z)
                textura_camaVelha[0])   
    
    desenha_objeto(program, verticeInicial_abobora, quantosVertices_abobora,
                0, #angulo
                0, 1, 0, #eixo de rotação (x, y, z)
                10, 0, 0, #translação (x, y, z)
                1, 1, 1, #escala (x, y, z)
                textura_abobora[0])
    
    desenha_objeto(program, verticeInicial_capa2, quantosVertices_capa2,
                0, #angulo
                0, 1, 0, #eixo de rotação (x, y, z)
                15, 0, 0, #translação (x, y, z)
                1, 1, 1, #escala (x, y, z)
                textura_capa2[0])
    
    desenha_objeto(program, verticeInicial_capaArrasta, quantosVertices_capaArrasta,
                0, #angulo
                0, 1, 0, #eixo de rotação (x, y, z)
                20, 0, 0, #translação (x, y, z)
                1, 1, 1, #escala (x, y, z)
                textura_capaArrasta[0])
    
    # para fazer o fantasma ter a transpatência que precisa, vamos precisar modificar o código do shader, mas por enquanto só vou desenhar ele aqui mesmo, e depois faço as modificações necessárias para a transparência se concordar.
    desenha_objeto(program, verticeInicial_fantasma_puido, quantosVertices_fantasma_puido,
                0, #angulo
                0, 1, 0, #eixo de rotação (x, y, z)
                25, 0, 0, #translação (x, y, z)
                1, 1, 1, #escala (x, y, z)
                textura_fantasma_puido[0])