from OpenGL.GL import *
from Projeto.graficos.texture import *
from Projeto.main import program

vertices_list = []    
textures_coord_list = []

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    objects = {}
    vertices = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue

        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])

        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces

    return model

'''
É possível encontrar, na Internet, modelos .obj cujas faces não sejam triângulos. Nesses casos, precisamos gerar triângulos a partir dos vértices da face.
A função abaixo retorna a sequência de vértices que permite isso. Créditos: Hélio Nogueira Cardoso e Danielle Modesti (SCC0650 - 2024/2).
'''

def circular_sliding_window_of_three(arr):
    if len(arr) == 3:
        return arr
    circular_arr = arr + [arr[0]]
    result = []
    for i in range(len(circular_arr) - 2):
        result.extend(circular_arr[i:i+3])
    return result

def desenha_objeto(verticeInicial,    quantosVertices, angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, textureId):

    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
           
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, textureId)
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, verticeInicial, quantosVertices) ## renderizando

numberTextures = 0

def load_obj_and_texture(objFile, texturesList):
    modelo = load_model_from_file(objFile)
    
    ### inserindo vertices do modelo no vetor de vertices
    verticeInicial = len(vertices_list)
    print('Processando modelo {}. Vertice inicial: {}'.format(objFile, len(vertices_list)))
    faces_visited = []
    for face in modelo['faces']:
        if face[2] not in faces_visited:
            faces_visited.append(face[2])
        for vertice_id in circular_sliding_window_of_three(face[0]):
            vertices_list.append(modelo['vertices'][vertice_id - 1])
        for texture_id in circular_sliding_window_of_three(face[1]):
            textures_coord_list.append(modelo['texture'][texture_id - 1])
        
    verticeFinal = len(vertices_list)
    print('Processando modelo {}. Vertice final: {}'.format(objFile, len(vertices_list)))
    
    ### carregando textura equivalente e definindo um id (buffer): use um id por textura!
    global numberTextures
    
    for i in range(len(texturesList)):
        load_texture_from_file(numberTextures,texturesList[i])
        numberTextures += 1
    
    return verticeInicial, verticeFinal - verticeInicial
    