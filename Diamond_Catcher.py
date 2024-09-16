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
    
def find_zone(x1,y1,x2,y2):
    
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
    #Convert to zone 0
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
    

    # iterate over x coordinates
    while x < x2:
        if d <= 0:
            d += dE
            x += 1
        else:
            d += dNE
            x += 1
            y += 1
        # Convert back from zone 0
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0)
    
def convert_coordinate(x,y):
    
    a = x - (500/2)
    b = (800/2) - y 
    return a,b


def generate_color() : 
    return [random.random(),random.random(),random.random()] 

#----------CLASS---------
class Diamond:
    def __init__(self):
        self.x = random.randint(-230,230)
        self.y = 370
        self.color = generate_color()
        self.iteration = 0
        
    def reset(self):
        self.x = random.randint(-230,230)
        self.y = 370
        self.color = generate_color()
        
        
class Catcher:
    def __init__(self):
        self.x = 0
        self.color = [1,1,1]



freeze = False
gameover=False
speed = 100

diamond = Diamond()
catcher = Catcher()


def draw_diamond():
    global diamond
    glPointSize(2)

    glColor3f(diamond.color[0], diamond.color[1], diamond.color[2])
    midpoint_line(diamond.x+10, diamond.y, diamond.x, diamond.y+15)
    midpoint_line(diamond.x+10, diamond.y, diamond.x, diamond.y-15)
    midpoint_line(diamond.x-10, diamond.y,diamond.x, diamond.y+15)
    midpoint_line(diamond.x-10, diamond.y, diamond.x, diamond.y-15)


def draw_home_screen():
    global catcher ,freeze
    #catcher
    glPointSize(3)
    glColor3f(catcher.color[0], catcher.color[1], catcher.color[2])
    midpoint_line(catcher.x+70, -360, catcher.x-70, -360)
    midpoint_line(catcher.x+60, -380, catcher.x+70, -360)
    midpoint_line(catcher.x+60, -380 ,catcher.x-60, -380)
    midpoint_line(catcher.x-60, -380, catcher.x-70, -360)

    #restart button
    glPointSize(4)
    glColor3f(0, 0.7, 0.7)
    midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_line(-210, 350, -190, 370)
    midpoint_line(-210, 350, -190, 330)
    
    
    #Cross button
    glPointSize(3)
    glColor3f(1, 0, 0)
    midpoint_line(210, 365, 180, 335)
    midpoint_line(210, 335, 180, 365)

    #pause button
    glPointSize(4)
    glColor3f(1, 0.5, 0.0)
    if freeze:
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else:
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)
        
def keyboardListener(key,x,y):
    if key == b'q':
        glutLeaveMainLoop()
        print("Goodbye! Score : ",diamond.iteration)
    

def specialKeyListener(key, x, y):
    global catcher, freeze
    if key== GLUT_KEY_RIGHT:		
        if catcher.x<180 and not freeze:
            catcher.x += 15
    if key== GLUT_KEY_LEFT:		
        if catcher.x>-180 and not freeze:
            catcher.x -= 15
    glutPostRedisplay()
    
    
def mouseListener(button,state,x,y):
    
    global freeze, diamond, gameover, catcher, speed

    
    #Restarting a game
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x,y)
        if -209 < c_x <-170 and 325 <c_y < 375:
            print("New Game")
            diamond.reset()
            gameover = False
            freeze = False
            diamond.iteration = 0
            speed = 100
            catcher.color = [1, 1, 1] 
        
        #Pausing the game 
        if -25 < c_x < 25 and 325 < c_y < 375:
            freeze = not freeze
            
        if 240< c_x < 160 and 360<c_y<275:
            glutLeaveMainLoop()
        
        

#---------- Funtion Calls ----------

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    
    glLoadIdentity()
  
    gluLookAt(0,0,314,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    draw_home_screen()
    draw_diamond()
    glutSwapBuffers()
    

def animate():
    cur_time = time.time()
    delta_time = cur_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = cur_time
    
    
    global freeze, diamond, catcher, gameover, speed
    if not freeze and not gameover:
        diamond.y -= (100+diamond.iteration*10) *delta_time
        if (diamond.y <= -365) and (catcher.x-70<= diamond.x <= catcher.x+70):
            
            diamond.iteration +=1
            speed += 40
            print("Score:",diamond.iteration) 
            diamond.reset()
            
        if diamond.y <= -400:
            catcher.color = [1,0,0]
            print("Game Over! Score:",diamond.iteration)
            diamond.reset()
            diamond.iteration = 0
            freeze = not freeze 
            gameover = True
            speed = 100
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



wind = glutCreateWindow(b"Catch the Diamonds!")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)	

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc( mouseListener)

glutMainLoop()		