# Author: Gustavo Lopes Tamiosso
# A script to generate a trajectory dataset 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import array, dtype, int8
from trajectory import *
import gc
DEFAULT_WIDHT = 800
DEFAULT_HEIGHT = 800
INITIAL_POSITION = (0, 0)

x_pos: int
y_pos: int
width = DEFAULT_WIDHT
height = DEFAULT_HEIGHT
array_size = 10
trajectories = numpy.ndarray(array_size, dtype=numpy.object)
last_index = 0

time = 0
clicking = False
frame_ms = 17
smooth_factor = 5

def init() -> None:
    global width, height
    glClearColor(0.10, 0.11, 0.13, 1)

def reshape(w, h):
    global width, height
    width = w
    height = h
    glViewport(0, 0, w, h)

def update(value) -> None:
    global clicking
    global time

    if(clicking):
        trajectories[last_index].add_timestamp((((x_pos/glutGet(GLUT_WINDOW_WIDTH))*2)-1), -1*(((y_pos/glutGet(GLUT_WINDOW_HEIGHT))*2)-1), time)
        time += frame_ms

    glutPostRedisplay()
    glutTimerFunc(frame_ms, update, 1)
def draw() -> None:
    global last_index
    global clicking
    glClear(GL_COLOR_BUFFER_BIT)
    glPushMatrix()
    glPushMatrix()
    max_index = 0
    if((last_index == 0 and clicking)):
        max_index = 1
    elif(last_index > 0 and clicking):
        max_index = last_index+1
    else:
        max_index = last_index
    for t in range(max_index):
            glColor4f(1, 0, 0, 1)
            glBegin(GL_LINES)
            for i in range(0, trajectories[t].last_index-1):
                glVertex2d(trajectories[t].draw_position[i][0], trajectories[t].draw_position[i][1])
                glVertex2d(trajectories[t].draw_position[i+1][0], trajectories[t].draw_position[i+1][1])
            glEnd()
    glPopMatrix()
    text0 = 'Press \'C\' to clear the trajectories created'
    text1 = 'Press \'S\' to save the tracjectories to files'
    text2 = 'Press \'Q\' to quit'
    printText((glutGet(GLUT_WINDOW_WIDTH)/2)-(len(text0)*9/2), glutGet(GLUT_WINDOW_HEIGHT)-(15), text0)
    printText((glutGet(GLUT_WINDOW_WIDTH)/2)-(len(text1)*9/2), glutGet(GLUT_WINDOW_HEIGHT)-(15*2), text1)
    printText((glutGet(GLUT_WINDOW_WIDTH)/2)-(len(text2)*9/2), glutGet(GLUT_WINDOW_HEIGHT)-(15*3), text2)
    glPopMatrix()
    glutSwapBuffers()

def keyboardHandler(key, x, y) -> None:
    global last_index
    if(key == b'q' or key == b'Q'):
        glutLeaveMainLoop()
    elif(key == b'c' or key == b'C'):
        for i in range(last_index):
            numpy.delete(trajectories, i)
        last_index = 0
    elif(key == b'p' or key == b'P'):
        for i in range(0, last_index):
            trajectories[i].plotAcceleration()
            trajectories[i].plotVelocity()
            trajectories[i].plotPosition()
    elif(key == b's' or key == b'S'):
        for i in range(0, last_index):
            trajectories[i].save()

def mouseHandler(button, state, x, y) -> None:
    global clicking, x_pos, y_pos
    global time
    global last_index
    global array_size
    global trajectories
    if(button == GLUT_LEFT and state == GLUT_DOWN):
        time = 0
        trajectories[last_index] = Trajectory(name=f'trajectory-{last_index}')
        trajectories[last_index].add_timestamp((((x/glutGet(GLUT_WINDOW_WIDTH))*2)-1), -1*(((y/glutGet(GLUT_WINDOW_HEIGHT))*2)-1), time)
        clicking = True
        x_pos = x
        y_pos = y
    elif(button == GLUT_LEFT and state == GLUT_UP):
        time = 0
        trajectories[last_index].smooth(smooth_factor)
        clicking = False
        last_index += 1
        if(last_index == array_size-1):
            array_size = int(array_size * 2)
            aux_trajectories = numpy.zeros(array_size, dtype=object)
            for i in range(last_index):
                aux_trajectories[i] = trajectories[i]
            trajectories = aux_trajectories

def motionHandler(x: int, y: int) -> None:
    global x_pos, y_pos
    x_pos = x
    y_pos = y

def printText( x,  y, text):
    glColor3f(1, 1, 1)
    glWindowPos2f(x, y)

    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15 , ctypes.c_int(ord(ch)))

def main() -> None:
    gc.enable()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)

    glutInitWindowSize(DEFAULT_WIDHT, DEFAULT_HEIGHT)
    glutInitWindowPosition(INITIAL_POSITION[0], INITIAL_POSITION[1])

    glutCreateWindow('Path generator for trajectories behaviour analysis')
    glutDisplayFunc(draw)
    glutTimerFunc(frame_ms, update, 1)
    glutMouseFunc(mouseHandler)
    glutMotionFunc(motionHandler)
    glutKeyboardFunc(keyboardHandler)
    glutReshapeFunc(reshape)

    init()

    glPushMatrix()
    glutMainLoop()

if __name__ == '__main__':
    main()
