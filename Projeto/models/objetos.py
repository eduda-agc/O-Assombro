from PIL import Image
from OpenGL.GL import *
from transformacoes_mat.transforms import *
import os  # para manipulação de caminhos de arquivos

vertices_list = []
textures_coord_list = []
normals_list = []  # NOVO

textures_ids = []  # guarda IDs reais de textura


def load_model_from_file(filename):
    """Loads a Wavefront OBJ file."""

    vertices = []
    texture_coords = []
    normals = []  # NOVO

    faces = []

    material = None

    for line in open(filename, "r"):
        if line.startswith('#'):
            continue

        values = line.split()

        if not values:
            continue

        # vértices
        if values[0] == 'v':
            vertices.append(values[1:4])

        # coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        # normais
        elif values[0] == 'vn':
            normals.append(values[1:4])

        # material
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]

        # faces
        elif values[0] == 'f':

            face = []
            face_texture = []
            face_normals = []

            for v in values[1:]:

                w = v.split('/')

                # índice do vértice
                face.append(int(w[0]))

                # índice da textura
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

                # índice da normal
                if len(w) >= 3 and len(w[2]) > 0:
                    face_normals.append(int(w[2]))
                else:
                    face_normals.append(0)

            faces.append(
                (
                    face,
                    face_texture,
                    face_normals,
                    material
                )
            )

    return {
        'vertices': vertices,
        'texture': texture_coords,
        'normals': normals,  # NOVO
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

    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open(img_textura).convert("RGBA")

    img_width, img_height = img.size

    image_data = img.tobytes("raw", "RGBA", 0, -1)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        img_width,
        img_height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        image_data
    )

    return texture_id


def get_mtl_from_obj(obj_path):

    try:
        with open(obj_path, 'r') as f:

            for line in f:

                if line.startswith('mtllib'):
                    return line.strip().split()[1]

    except:
        print(f"Erro ao ler OBJ: {obj_path}")

    return None


def load_mtl_file(mtl_path):

    textures = []

    try:
        with open(mtl_path, 'r') as f:

            for line in f:

                if line.startswith('map_Kd'):
                    texture_file = line.strip().split()[1]
                    textures.append(texture_file)

    except:
        print(f"Erro ao ler MTL: {mtl_path}")

    return textures


def load_obj_and_texture(objFile, texturesList=None):

    modelo = load_model_from_file(objFile)

    verticeInicial = len(vertices_list)

    print(f'Processando modelo {objFile}. Vertice inicial: {verticeInicial}')

    faces_visited = []

    for face in modelo['faces']:

        # material agora está no índice 3
        if face[3] not in faces_visited:
            faces_visited.append(face[3])

        # vértices
        for vertice_id in circular_sliding_window_of_three(face[0]):

            vertices_list.append(
                modelo['vertices'][vertice_id - 1]
            )

        # texturas
        for texture_id in circular_sliding_window_of_three(face[1]):

            if texture_id > 0:
                textures_coord_list.append(
                    modelo['texture'][texture_id - 1]
                )
            else:
                textures_coord_list.append([0.0, 0.0])

        # normais
        for normal_id in circular_sliding_window_of_three(face[2]):

            if normal_id > 0:
                normals_list.append(
                    modelo['normals'][normal_id - 1]
                )
            else:
                normals_list.append([0.0, 1.0, 0.0])

    verticeFinal = len(vertices_list)

    print(f'Processando modelo {objFile}. Vertice final: {verticeFinal}')

    texture_ids_local = []

    # se não passar textura, tenta usar MTL
    if texturesList is None:

        mtl_file = get_mtl_from_obj(objFile)

        if mtl_file:

            base_path = os.path.dirname(objFile)

            mtl_path = os.path.join(base_path, mtl_file)

            texture_files = load_mtl_file(mtl_path)

            texturesList = [
                os.path.join(base_path, tex)
                for tex in texture_files
            ]

            print(f"Texturas encontradas via MTL: {texturesList}")

        else:
            print("Nenhum MTL encontrado.")

    # carregar texturas
    if texturesList:

        for tex in texturesList:

            tex_id = load_texture_from_file(tex)

            textures_ids.append(tex_id)

            texture_ids_local.append(tex_id)

    return (
        verticeInicial,
        verticeFinal - verticeInicial,
        texture_ids_local
    )


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
    textureId,
    material_diffuse=1.0,
    material_specular=0.25,
    receive_candle_light=False
):

    mat_model = model(
        angle,
        r_x,
        r_y,
        r_z,
        t_x,
        t_y,
        t_z,
        s_x,
        s_y,
        s_z
    )

    loc_model = glGetUniformLocation(program, "model")

    glUniformMatrix4fv(
        loc_model,
        1,
        GL_TRUE,
        mat_model
    )

    if textureId != 0:
        glBindTexture(GL_TEXTURE_2D, textureId)

    glUniform1f(
        glGetUniformLocation(program, "materialDiffuse"),
        material_diffuse
    )

    glUniform1f(
        glGetUniformLocation(program, "materialSpecular"),
        material_specular
    )

    glUniform1i(
        glGetUniformLocation(program, "receiveCandleLight"),
        receive_candle_light
    )

    glDrawArrays(
        GL_TRIANGLES,
        verticeInicial,
        quantosVertices
    )
