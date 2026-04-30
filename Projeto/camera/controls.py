import glfw
from OpenGL.GL import *
import glm
import math 
import models.lista_objetos as objs

# camera control variables
#cameraPos   = glm.vec3(0.0,  0.0,  1.0);
#cameraFront = glm.vec3(0.0,  0.0, -1.0);
#cameraUp    = glm.vec3(0.0,  1.0,  0.0);

# camera
cameraPos   = glm.vec3(15.0, -2.5, 9)
cameraFront = glm.vec3(0.0, 0.0, 1.0)
cameraUp    = glm.vec3(0.0, 1.0, 0.0)

# "head bob"
headbob_enabled = True
headbob_phase = 0.0
headbob_offset = glm.vec3(0.0, 0.0, 0.0)

move_forward = False
move_backward = False
move_left = False
move_right = False

firstMouse = True
yaw   = -90.0	# yaw is initialized to -90.0 degrees since a yaw of 0.0 results in a direction vector pointing to the right so we initially rotate a bit to the left.
pitch =  0.0
lastX = 0
lastY = 0

polygonal_mode = False

def init_camera(largura, altura):
    global lastX, lastY
    lastX = largura / 2
    lastY = altura / 2
    
fov   =  45.0

# timing
deltaTime = 0.0	# time between current frame and last frame
lastFrame = 0.0

def key_event(window, key, scancode, action, mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode
    global move_forward, move_backward, move_left, move_right
    global headbob_enabled

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_P and action == glfw.PRESS:
        polygonal_mode = not polygonal_mode

    #tecla para ligar/desligar o head bob
    if key == glfw.KEY_H and action == glfw.PRESS:
        headbob_enabled = not headbob_enabled

    cameraSpeed = 15 * deltaTime

    LIMITE = 30  

    cameraSpeed = 15 * deltaTime

   # -------- FRENTE --------
    if key == glfw.KEY_W:
        move_forward = (action == glfw.PRESS or action == glfw.REPEAT)
        if move_forward:
            direcao = glm.vec3(cameraFront.x, 0.0, cameraFront.z)

            # evita bug se olhar totalmente pra cima/baixo
            if glm.length(direcao) > 0:
                direcao = glm.normalize(direcao)

            nova_pos = cameraPos + direcao * cameraSpeed

            if -LIMITE <= nova_pos.x <= LIMITE and -LIMITE <= nova_pos.z <= LIMITE:
                cameraPos = nova_pos

    # -------- TRÁS --------
    if key == glfw.KEY_S:
        move_backward = (action == glfw.PRESS or action == glfw.REPEAT)
        if move_backward:
            direcao = glm.vec3(cameraFront.x, 0.0, cameraFront.z)

            if glm.length(direcao) > 0:
                direcao = glm.normalize(direcao)

            nova_pos = cameraPos - direcao * cameraSpeed

            if -LIMITE <= nova_pos.x <= LIMITE and -LIMITE <= nova_pos.z <= LIMITE:
                cameraPos = nova_pos

    # -------- ESQUERDA --------
    if key == glfw.KEY_A:
        move_left = (action == glfw.PRESS or action == glfw.REPEAT)
        if move_left:
            direita = glm.normalize(glm.cross(cameraFront, cameraUp))
            nova_pos = cameraPos - direita * cameraSpeed

            if -LIMITE <= nova_pos.x <= LIMITE and -LIMITE <= nova_pos.z <= LIMITE:
                cameraPos = nova_pos

    # -------- DIREITA --------
    if key == glfw.KEY_D:
        move_right = (action == glfw.PRESS or action == glfw.REPEAT)
        if move_right:
            direita = glm.normalize(glm.cross(cameraFront, cameraUp))
            nova_pos = cameraPos + direita * cameraSpeed

            if -LIMITE <= nova_pos.x <= LIMITE and -LIMITE <= nova_pos.z <= LIMITE:
                cameraPos = nova_pos

    if key == glfw.KEY_UP and (action == glfw.PRESS or action == glfw.REPEAT):
        if cameraPos.y < 10:  # limite superior
            cameraPos.y += cameraSpeed

    if key == glfw.KEY_DOWN and (action == glfw.PRESS or action == glfw.REPEAT):
        if cameraPos.y > -5:  # limite inferior
            cameraPos.y -= cameraSpeed

    if key == glfw.KEY_LEFT and (action == glfw.PRESS or action == glfw.REPEAT):
         objs.carro_pos[2] += 0.1  # move para trás

    if key == glfw.KEY_RIGHT and (action == glfw.PRESS or action == glfw.REPEAT):
         objs.carro_pos[2] -= 0.1  # move para frente     
         
    if key == glfw.KEY_T:
            objs.cadeira1_pos[0] += 0.05  # move no eixo X

    if key == glfw.KEY_G:
            objs.cadeira1_pos[0] -= 0.05

        # ---- ROTACAO (cadeira 2) ----
    if key == glfw.KEY_R:
            objs.cadeira2_rot += 5  # gira

    if key == glfw.KEY_F:
            objs.cadeira2_rot -= 5

    if key == glfw.KEY_Y:
            objs.mesa_posicao[1] += 0.05  # sobe

    if key == glfw.KEY_H:
            objs.mesa_posicao[1] -= 0.05  # desce
    
    if key == glfw.KEY_U:
            objs.fantasma_scale += 0.05  # aumenta a escala

    if key == glfw.KEY_J:
            objs.fantasma_scale -= 0.05  # diminui a escala
    
    if key == glfw.KEY_I:
            objs.abobora_angle += 3  # aumenta a escala

    if key == glfw.KEY_K:
            objs.abobora_angle -= 3  # diminui a escala

            

    if action == glfw.RELEASE:
        if key == glfw.KEY_W:
            move_forward = False
        if key == glfw.KEY_S:
            move_backward = False
        if key == glfw.KEY_A:
            move_left = False
        if key == glfw.KEY_D:
            move_right = False
    # ---- TRANSLACAO (cadeira 1) ----
        

# glfw: whenever the mouse moves, this callback is called
# -------------------------------------------------------
def mouse_callback(window, xpos, ypos):
    global cameraFront, lastX, lastY, firstMouse, yaw, pitch
   
    if (firstMouse):

        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos # reversed since y-coordinates go from bottom to top
    lastX = xpos
    lastY = ypos

    sensitivity = 0.1 # change this value to your liking
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    # make sure that when pitch is out of bounds, screen doesn't get flipped
    if (pitch > 89.0):
        pitch = 89.0
    if (pitch < -89.0):
        pitch = -89.0

    front = glm.vec3()
    front.x = glm.cos(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    front.y = glm.sin(glm.radians(pitch))
    front.z = glm.sin(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    cameraFront = glm.normalize(front)

# glfw: whenever the mouse scroll wheel scrolls, this callback is called
# ----------------------------------------------------------------------
def scroll_callback(window, xoffset, yoffset):
    global fov

    fov -= yoffset
    if (fov < 1.0):
        fov = 1.0
    if (fov > 45.0):
        fov = 45.0
    

#calcula o balanço

def update_headbob():
    global headbob_phase, headbob_offset

    moving = move_forward or move_backward or move_left or move_right

    if headbob_enabled and moving:
        #intensidade média estilo FPS
        bob_speed = 12.0
        bob_side = 0.15  
        bob_up = 0.10     

        headbob_phase += deltaTime * bob_speed

        right = glm.normalize(glm.cross(cameraFront, cameraUp))

        target_offset = (
            right * math.sin(headbob_phase) * bob_side +
            cameraUp * abs(math.cos(headbob_phase * 2.0)) * bob_up
        )
    else:
        target_offset = glm.vec3(0.0, 0.0, 0.0)

    #suaviza a transição quando começa/para de andar
    smooth = min(1.0, deltaTime * 12.0)
    headbob_offset += (target_offset - headbob_offset) * smooth
