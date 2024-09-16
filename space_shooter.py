import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glFlush()
    
#----- MIdPoint Line Algorithm -----
    
def convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)


def convert_from_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)
    
def find_zone(x1,y1,x2 ,y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6
    return zone 


def midpoint_line(x1, y1, x2, y2):
   
    zone = find_zone(x1, y1, x2, y2)
    
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    plot_point(x0, y0)
    

    
    while x < x2:
        if d <= 0:
            d += dE
            x += 1
        else:
            d += dNE
            x += 1
            y += 1
        #original coordinates
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0)
        
def midpointCircle(radius, center_x=0, center_y=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + center_x, y + center_y)
        glVertex2f(x + center_x, -y + center_y)
        glVertex2f(-x + center_x, y + center_y)
        glVertex2f(-x + center_x, -y + center_y)
        glVertex2f(y + center_x, x + center_y)
        glVertex2f(y + center_x, -x + center_y)
        glVertex2f(-y + center_x, x + center_y)
        glVertex2f(-y + center_x, -x + center_y)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2*x - 2*y + 5
            y -= 1
        x += 1
    glEnd()
    
def convert_coordinate(x,y):
    a = x - (500/2)
    b = (800/2) - y 
    return a,b

def generate_color() : 
    return [random.random(),random.random(),random.random()] 

#-----class-----
class Bubble:
    def __init__(self):
        self.x = random.randint(-230,230)
        self.y = 365
        self.r = random.randint(10,30)
        self.color = generate_color()
        
class Shooter:
    def __init__(self):
        self.x =0
        self.color = [1,1,1]
        


bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()] 
bubble.sort(key=lambda b: b.y) 
score = 0
fire = []
misfires= 0
freeze = False
gameover=0 
shooter = Shooter()


def draw_fire():
    global fire
    glPointSize(2)
    glColor3f(.8,  .4, 0) 
    for i in fire:
        midpointCircle(5, i[0], i[1])

def draw_bubble():
    global bubble
    glPointSize(3)
    for i in range(len(bubble)):
        if i ==0 :
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointCircle(bubble[i].r, bubble[i].x, bubble[i].y)
            
        elif (bubble[i-1].y<(330 -2*bubble[i].r -2*bubble[i-1].r)) or (abs(bubble[i-1].x-bubble[i].x)> (2*bubble[i-1].r+2*bubble[i].r +10) ):
                glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
                midpointCircle(bubble[i].r, bubble[i].x, bubble[i].y)
    
def draw_home_screen():

    global shooter

    #shooter
    glPointSize(2)
    glColor3f(shooter.color[0], shooter.color[1], shooter.color[2])
    midpointCircle(15, center_x=shooter.x, center_y=-365)


    #restart button
    glPointSize(4)
    glColor3f(0, 0.7, 0.7)
    midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_line(-210, 350, -190, 370)
    midpoint_line(-210, 350, -190, 330)


    #Cross Button
    glPointSize(3)
    glColor3f(1, 0, 0)
    midpoint_line(210, 365, 180, 335)
    midpoint_line(210, 335, 180, 365)

    #MPause Button
    glPointSize(4)
    glColor3f(1, .5, 0)
    if freeze:
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else:
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)
    
def keyboardListener(key,x,y):
    
    global fire,freeze,gameover,shooter
    
    if key == b' ':
        if not freeze and gameover<5:
            fire.append([shooter.x,-365])
            
    if key == b'd' :
        if shooter.x < 230 and not freeze:
            shooter.x += 10
            
    if key == b'a' :
        if shooter.x > -230 and not freeze:
            shooter.x -= 10
    glutPostRedisplay()
            
    
 
def mouseListener(button, state, x, y):
    global freeze, gameover, cshooter, score, bubble, fire, misfires
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            freeze= False
            print('Starting Over')
            bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
            bubble.sort(key=lambda b: b.x)
            score = 0
            gameover = 0
            misfires = 0
            fire  = []

        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Score:', score)
            print("Misfire:", misfires)
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 365:
            freeze = not freeze
    
    glutPostRedisplay()
    


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    
    glLoadIdentity()
  
    gluLookAt(0,0,314,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    draw_home_screen()
    draw_bubble()
    draw_fire()
    glutSwapBuffers()
    
    
    
def animate():
    cur_time = time.time()
    delta_time = cur_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = cur_time
    
    global freeze, bubble, shooter, gameover, score, bullet, misfires
    
    if not freeze and gameover<3  and misfires<3:
        idx = []
        for i in range(len(fire)):
            if  fire[i][1]< 365:
                fire[i][1] += 10
            else:
                
                misfires += 1
                idx.append(i)
                print("Misfire:",misfires)
                
        for j in idx:
            del fire[j]
                
        for i in range(len(bubble)):
            if i == 0:
                if bubble[i].y > -365 :
                    bubble[i].y -= (10+score*5)* delta_time
                else :
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)
                    
            elif (bubble[i-1].y<(330 -2*bubble[i].r -2*bubble[i-1].r)) or (abs(bubble[i-1].x-bubble[i].x)> (2*bubble[i-1].r+2*bubble[i].r +10) ):
                if bubble[i].y > -400 :
                    bubble[i].y -= (10+score*5)* delta_time
                else :
                    gameover += 1
                    
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)
                    
        for i in range(len(bubble)):
            if abs(bubble[i].y- -365) <(bubble[i].r) and abs(bubble[i].x- shooter.x)< (bubble[i].r+15):
                gameover+=404
                    
            for j in range(len(fire)):
                if abs(bubble[i].y- fire[j][1])< (bubble[i].r+5+3) and abs(bubble[i].x- fire[j][0])< (bubble[i].r+5+3):
                    score+=1
                    print("Score:", score)
                    print("Misfire:", misfires)
                    del bubble[i]
                    del fire[j]
                    bubble.append(Bubble())
                   # bubble.sort(key=lambda b: b.y)
                    
    elif (gameover>=3 or misfires>=3) and not freeze:
        print("Game Over! Score:", score)  
        print("Misfire:", misfires)
        freeze= True

    time.sleep(2/60)
    glutPostRedisplay()
        


    
def init():

    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	(500/800),	1,	1000.0) 

glutInit()
glutInitWindowSize(500, 800) 
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 


wind = glutCreateWindow(b"Shoot The Circles")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)	
glutKeyboardFunc(keyboardListener)
#glutSpecialFunc(specialKeyListener)
glutMouseFunc( mouseListener)

glutMainLoop()		