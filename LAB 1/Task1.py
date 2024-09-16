from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 

def draw_points(x, y):
    glPointSize(10) 
    glBegin(GL_POINTS)
    glVertex2f(x,y) 
    glEnd()

def draw_Line(x0,y0,x1,y1):
    glLineWidth(5) 
    glBegin(GL_LINES)
    glColor3f(255,0,0)
    glVertex2f(x0,y0)
    glColor3f(0.0,0.0,255)
    glVertex2f(x1,y1) 
    glEnd()
    
def draw_Roof(p1,p2,p3,height):
    
    glLineWidth(1) 
    glBegin(GL_TRIANGLES)
    glColor3f(1.0,1.0,1.0)
    glVertex2f(p1,height)
    glColor3f(1.0,1.0,1.0)
    glVertex2f(p2,p2)
    glColor3f(1.0,1.0,1.0)
    glVertex2f(p3,height)
    glEnd()

def draw_door(left,right,base,height):
    
    draw_Line(left,base,left,height)
    draw_Line(left,height,right,height)
    draw_Line(right,height,right,base)
    draw_points(325,110)
    
def draw_window(initial_x,initial_y):
   
   draw_Line(initial_x,initial_y,initial_x,initial_y+100)
   draw_Line(initial_x,initial_y+100,initial_x+100,initial_y+100)
   draw_Line(initial_x+100,initial_y+100,initial_x+100,initial_y)
   draw_Line(initial_x+100,initial_y,initial_x,initial_y)
   draw_Line(initial_x,initial_y+50,initial_x+100,initial_y+50)
   draw_Line(initial_x+50,initial_y+100,initial_x+50,initial_y)
    
    
def draw_House():
    
    draw_Roof(200,500,800,300)
    draw_Line(220,300,220,50)
    draw_Line(780,300,780,50)
    draw_Line(220,50,780,50)
    draw_door(270,340,50,200)
    draw_window(550,150)
    
   
border1 = 200
border2 = 800 
speed = 0.01
angle = 0.0
raindrop_arr = []
bg = (0.0,0.0,0.0,0.0) 

def  draw_rainDrop(x,y):
    glPointSize(5) 
    glBegin(GL_POINTS)
    glColor3f(1.0,1.0,1.0)
    glVertex2f(x,y) 
    glEnd()

def rain():
    
    global angle,speed 
    for i in range(0,len(raindrop_arr)) :
        update_x, update_y = raindrop_arr[i] 
        
        update_x += speed+angle
        update_y -= 1
        
        if (update_y < 300) or (300<update_x<800 and 400<update_y<900) :
            update_x = random.uniform(300,800)
            update_y = random.uniform(900,400)
        raindrop_arr[i] = (update_x,update_y)


def animate() :
    rain()
    glutPostRedisplay()
    

def specialKeyListener(key, x, y): 
    global angle 
    if key==GLUT_KEY_RIGHT:
        angle += 0.1
        print("Tilt Right")
    if key== GLUT_KEY_LEFT:		
        angle -= 0.1
        print("Tilt Left")
    
    glutPostRedisplay()




    
def iterate():
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,1000.0,0.0,1000.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
def showScreen():
    global speed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 1.0) #konokichur color set (RGB)
    #call the draw methods here
    
    draw_House()
    rain()
    for k in raindrop_arr :
        draw_rainDrop(k[0],k[1])
    
        
    glutSwapBuffers()
    
glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE |GLUT_RGBA)
glutInitWindowSize(1000,1000) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
#glutKeyboardFunc(keyboardListener)
glutIdleFunc(animate)

for j in range(50):
    x2 = random.uniform(300,800)
    y2= random.uniform(900,400)
    raindrop_arr.append((x2, y2))

glutMainLoop()