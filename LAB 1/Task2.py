from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 

def draw_points(x, y,color):
    glPointSize(10) 
    glBegin(GL_POINTS)
    glColor3f(color[0],color[1],color[2])
    glVertex2f(x,y) 
    glEnd()
    
points_set = []
speed = 0.05


def generate_point() : 
    x = random.uniform(100,200)
    y = random.uniform(100,200)
    return x,y

def generate_color() : 
    return [random.random(),random.random(),random.random()]    

def convert(x,y):
    a = x - (400/2)
    b = (400/2) - y
    return a,b

def mouse_listener(button,state,x,y):
    
    global points_set
    if button == GLUT_RIGHT_BUTTON:
        if(state == GLUT_DOWN):
            X,Y = convert(x,y)
            points_set.append([X,Y,generate_color()])
             
                
    if button == GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            for point in points_set:
                if point[2] != [1.0,1.0,1.0]:
                    point[2] = [1.0,1.0,1.0]
                else:
                    point[2] = generate_color()
    glutPostRedisplay()


def keyboardListener(key,x,y):
    global speed
    if key ==b" ":
        if speed != 0:
            speed= 0
        else :
            speed = 0.05
        glutPostRedisplay()

def specialKey(key,x,y):
    
    global points_set,speed
    if key == GLUT_KEY_UP:
        speed += .01
        print("Speed Increased")
    if key == GLUT_KEY_DOWN:
        speed -= .01
        print("Speed Decreased")
    
    
    glutPostRedisplay()
  
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,500.0,0.0,500.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()  
    
def drawBoundary():
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(1.0,0.0,0.0)
    glVertex2f(0,200)
    glVertex2f(200,200)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(200,200)
    glVertex2f(200,0)
    glColor3f(1.0,0.0,0.0)
    glVertex2f(200,0)
    glVertex2f(0,0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0,0)
    glVertex2f(0,200)
    glEnd()
    

def animate():
    global points_set,speed
    glutPostRedisplay()
    movement = [1,-1]
    for point in points_set:
        point[0] = (point[0]+speed)%200
        point[1] = (point[1]+speed)%200
             
        
    
   

def display():
    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1,1,1,1);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    #//now give three info
    #//1. where is the camera (viewer)?
    #//2. where is the camera looking?
    #//3. Which direction is the camera's UP direction?
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    drawBoundary()
    for point in points_set:
        draw_points(point[0],point[1],point[2]) 
        print("Point Created")
    glutSwapBuffers()


def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize thsssssse matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(100,	1,	1,	1000.0)   
    
glutInit()
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE |GLUT_RGBA)
glutInitWindowSize(500,500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKey)
glutMouseFunc(mouse_listener)
glutMainLoop()