from PIL import Image
from OpenGL.GL import *
from transformacoes_mat.transforms import *

vertices_list = []    
textures_coord_list = []
textures_ids = []  # 🔥 guarda IDs reais de textura


def load_model_from_file(filename):
    """Loads a Wavefront OBJ file."""
    vertices = []
    texture_coords = []
    faces = []

    material = None

    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue

        if values[0] == 'v':
            vertices.append(values[1:4])

        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

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

    return {
        'vertices': vertices,
        'texture': texture_coords,
        'faces': faces
    }


def circular_sliding_window_of_three(arr):
    if len(arr) == 3:
        return arr

    circular_arr = arr + [arr[0]]
    result = []

    for i in range(len(circular_arr) - 2):
        result.extend(circular_arr[i:i+3])

    return result


def load_texture_from_file(img_textura):
    texture_id = glGenTextures(1)  # 🔥 cria textura real
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open(img_textura)
    img_width, img_height = img.size
    image_data = img.tobytes("raw", "RGB", 0, -1)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB,
        img_width,
        img_height,
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        image_data
    )

    return texture_id


def load_obj_and_texture(objFile, texturesList):
    modelo = load_model_from_file(objFile)

    verticeInicial = len(vertices_list)
    print(f'Processando modelo {objFile}. Vertice inicial: {verticeInicial}')

    faces_visited = []

    for face in modelo['faces']:
        if face[2] not in faces_visited:
            faces_visited.append(face[2])

        # vertices
        for vertice_id in circular_sliding_window_of_three(face[0]):
            vertices_list.append(modelo['vertices'][vertice_id - 1])

        # texturas
        for texture_id in circular_sliding_window_of_three(face[1]):
            textures_coord_list.append(modelo['texture'][texture_id - 1])

    verticeFinal = len(vertices_list)
    print(f'Processando modelo {objFile}. Vertice final: {verticeFinal}')

    # 🔥 carregar texturas corretamente
    texture_ids_local = []

    for tex in texturesList:
        tex_id = load_texture_from_file(tex)
        textures_ids.append(tex_id)
        texture_ids_local.append(tex_id)

    return verticeInicial, verticeFinal - verticeInicial, texture_ids_local


def desenha_objeto(program, verticeInicial, quantosVertices,
                  angle, r_x, r_y, r_z,
                  t_x, t_y, t_z,
                  s_x, s_y, s_z,
                  textureId):

    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

    # 🔥 bind correto da textura
    glBindTexture(GL_TEXTURE_2D, textureId)

    glDrawArrays(GL_TRIANGLES, verticeInicial, quantosVertices)