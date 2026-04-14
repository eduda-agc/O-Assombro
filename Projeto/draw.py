

from Projeto.transforms import model
from OpenGL.GL import *

def desenha_objeto(vertice_inicio, quantos_vertices, angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, textureId):

    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
           
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, textureId)
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, vertice_inicio, quantos_vertices) ## renderizando