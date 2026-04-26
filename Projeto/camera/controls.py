import glfw
from OpenGL.GL import *
import glm
import math 

# camera control variables
#cameraPos   = glm.vec3(0.0,  0.0,  1.0);
#cameraFront = glm.vec3(0.0,  0.0, -1.0);
#cameraUp    = glm.vec3(0.0,  1.0,  0.0);

# camera
cameraPos   = glm.vec3(0.0, 0.0, 3.0)
cameraFront = glm.vec3(0.0, 0.0, -1.0)
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

    cameraSpeed = 9 * deltaTime

    if key == glfw.KEY_W:
        move_forward = (action == glfw.PRESS or action == glfw.REPEAT)
        if move_forward:
            cameraPos += cameraSpeed * cameraFront

    if key == glfw.KEY_S:
        move_backward = (action == glfw.PRESS or action == glfw.REPEAT)
        if move_backward:
            cameraPos -= cameraSpeed * cameraFront

    if key == glfw.KEY_A:
        move_left = (action == glfw.PRESS or action == glfw.REPEAT)
        if move_left:
            cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed

    if key == glfw.KEY_D:
        move_right = (action == glfw.PRESS or action == glfw.REPEAT)
        if move_right:
            cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed

    if action == glfw.RELEASE:
        if key == glfw.KEY_W:
            move_forward = False
        if key == glfw.KEY_S:
            move_backward = False
        if key == glfw.KEY_A:
            move_left = False
        if key == glfw.KEY_D:
            move_right = False
        

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
