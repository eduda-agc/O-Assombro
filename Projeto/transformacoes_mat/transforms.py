import math
import glm
import numpy as np
import camera.controls as controls

def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
       
    # aplicando translacao (terceira operação a ser executada)
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao (segunda operação a ser executada)
    if angle!=0:
        matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    
    # aplicando escala (primeira operação a ser executada)
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    
    matrix_transform = np.array(matrix_transform)
    
    return matrix_transform

def view():
    global cameraPos, cameraFront, cameraUp
    mat_view = glm.lookAt(controls.cameraPos, controls.cameraPos + controls.cameraFront, controls.cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

def projection(altura, largura):
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(controls.fov), largura/altura, 0.1, 100.0)
    
    mat_projection = np.array(mat_projection)    
    return mat_projection

#funções para gerar as matrizes de transformação mais facilmente 
def identidade():
    return np.array([
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    ], dtype=np.float32)

def translacao(x, y, z):
    return np.array([
        1.0, 0.0, 0.0, x,
        0.0, 1.0, 0.0, y,
        0.0, 0.0, 1.0, z,
        0.0, 0.0, 0.0, 1.0
    ], dtype=np.float32)

def escala(sx, sy, sz):
    return np.array([
        sx, 0.0, 0.0, 0.0,
        0.0, sy, 0.0, 0.0,
        0.0, 0.0, sz, 0.0,
        0.0, 0.0, 0.0, 1.0
    ], dtype=np.float32)

def rotacao_z(angulo):
    c = math.cos(angulo)
    s = math.sin(angulo)
    return np.array([
         c, -s, 0.0, 0.0,
         s,  c, 0.0, 0.0,
       0.0,0.0, 1.0, 0.0,
       0.0,0.0, 0.0, 1.0
    ], dtype=np.float32)

def rotacao_y(angulo):
    c = math.cos(angulo)
    s = math.sin(angulo)
    return np.array([
         c, 0.0,  s, 0.0,
       0.0, 1.0, 0.0, 0.0,
        -s, 0.0,  c, 0.0,
       0.0, 0.0, 0.0, 1.0
    ], dtype=np.float32)

def rotacao_x(angulo):
    c = math.cos(angulo)
    s = math.sin(angulo)
    return np.array([
       1.0, 0.0, 0.0, 0.0,
       0.0,  c, -s, 0.0,
       0.0,  s,  c, 0.0,
       0.0, 0.0, 0.0, 1.0
    ], dtype=np.float32)