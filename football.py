from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, sys

WIDTH, HEIGHT = 900, 600
MAX_ATTEMPTS = 10

aim_x = ball_x = keeper_x = 450
ball_y = 110
shot_active = False
shot_t = 0.0
result = ""
score = attempts = frame = 0


def circle(x, y, r):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(101):
        a = 2 * math.pi * i / 100
        glVertex2f(x+r*math.cos(a), y+r*math.sin(a))
    glEnd()


def rect(x, y, w, h):
    glBegin(GL_QUADS)
    for p in [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]:
        glVertex2f(*p)
    glEnd()


def text(x, y, s):
    glColor3f(1,1,1)
    glRasterPos2f(x,y)
    for ch in s:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(ch))


def drawSky():
    glColor3f(.35,.70,.95)
    rect(0,350,900,250)
    glColor3f(1,.85,.1)
    circle(790,520,38)
    glColor3f(1,1,1)
    for x,y in [(120,510),(350,535),(600,490)]:
        circle(x,y,20)
        circle(x+25,y+10,25)
        circle(x+50,y,20)


def drawStadium():
    glColor3f(.35,.20,.35)
    rect(0,300,900,100)

    colors=[(1,.2,.2),(1,1,.2),(.2,.8,1),(1,1,1),(.2,1,.3)]
    for i in range(45):
        glColor3f(*colors[i%5])
        circle(15+i*20,320+(i%3)*18,5)

    glColor3f(.25,.25,.30)
    rect(0,395,900,10)


def drawGround():
    glColor3f(.12,.55,.20)
    rect(0,0,900,350)

    for i in range(9):
        glColor3f(*((.15,.62,.24) if i%2==0 else (.10,.50,.18)))
        rect(i*100,0,100,350)

    glColor3f(1,1,1)
    glLineWidth(3)

    def outline(points):
        glBegin(GL_LINE_LOOP)
        for p in points:
            glVertex2f(*p)
        glEnd()

    outline([(220,350),(680,350),(680,120),(220,120)])
    outline([(330,350),(570,350),(570,240),(330,240)])

    circle(450,130,4)
    glBegin(GL_LINES)
    glVertex2f(0,300)
    glVertex2f(900,300)
    glEnd()


def drawGoal():
    glColor3f(.85,.88,.90)
    rect(300,390,300,115)

    glColor3f(.45,.50,.55)
    glLineWidth(1)
    glBegin(GL_LINES)
    for x in range(300,601,20):
        glVertex2f(x,390)
        glVertex2f(x,505)
    for y in range(390,506,20):
        glVertex2f(300,y)
        glVertex2f(600,y)
    glEnd()

    glColor3f(1,1,1)
    glLineWidth(8)
    glBegin(GL_LINE_LOOP)
    for p in [(300,390),(600,390),(600,505),(300,505)]:
        glVertex2f(*p)
    glEnd()
    glLineWidth(1)


def drawGoalkeeper():
    glPushMatrix()
    glTranslatef(keeper_x,410,0)

    glColor3f(1,.45,.05)
    rect(-22,-35,44,55)

    glColor3f(.95,.70,.50)
    circle(0,35,15)
    glColor3f(.1,.08,.05)
    circle(0,46,12)

    glColor3f(.95,.70,.50)
    glBegin(GL_QUADS)
    for p in [(-22,5),(-45,20),(-52,10),(-22,-5),
              (22,5),(45,20),(52,10),(22,-5)]:
        glVertex2f(*p)
    glEnd()

    glColor3f(1,1,0)
    circle(-50,15,9)
    circle(50,15,9)

    glColor3f(.08,.08,.12)
    rect(-20,-65,15,30)
    rect(5,-65,15,30)
    glPopMatrix()


def drawPlayer():
    glPushMatrix()
    glTranslatef(450,55,0)

    glColor3f(.1,.2,.85)
    rect(-18,0,36,40)

    glColor3f(.95,.70,.50)
    circle(0,52,13)

    glColor3f(.1,.07,.04)
    circle(0,61,10)

    glColor3f(.08,.08,.08)
    rect(-17,-25,12,27)
    rect(5,-25,12,27)

    glColor3f(1,1,1)
    rect(-20,-29,17,7)
    rect(5,-29,17,7)
    glPopMatrix()


def drawBall(x,y,scale=1):
    glPushMatrix()
    glTranslatef(x,y,0)
    glScalef(scale,scale,1)

    glColor3f(.08,.25,.08)
    circle(3,-4,11)

    glColor3f(1,1,1)
    circle(0,0,12)

    glColor3f(.05,.05,.05)
    for px,py,r in [(0,0,4),(-6,5,2.5),(7,5,2.5),
                    (-6,-6,2.5),(7,-6,2.5)]:
        circle(px,py,r)
    glPopMatrix()


def drawAim():
    if not shot_active and attempts < MAX_ATTEMPTS:
        glColor3f(1,1,0)
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2f(450,125)
        glVertex2f(aim_x,390)
        glEnd()
        glLineWidth(1)


def drawHUD():
    glColor3f(.05,.05,.15)
    rect(0,565,900,35)

    text(25,580,"PENALTY SHOOTOUT GAME")
    text(600,580,"SCORE: "+str(score))
    text(760,580,"SHOT: "+str(attempts)+"/10")

    text(20,20,"LEFT / RIGHT: AIM")
    text(330,20,"SPACE: SHOOT")
    text(700,20,"R: RESTART")

    if result:
        glColor3f(1,1,0)
        text(350,535,result)


def drawScene():
    drawSky()
    drawStadium()
    drawGround()
    drawGoal()
    drawPlayer()
    drawGoalkeeper()
    drawAim()

    if shot_active:
        drawBall(ball_x,ball_y,1-.55*shot_t)
    else:
        drawBall(450,110)

    drawHUD()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,WIDTH,0,HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    drawScene()
    glutSwapBuffers()


def shoot():
    global shot_active,shot_t,attempts,result

    if not shot_active and attempts < MAX_ATTEMPTS:
        shot_active=True
        shot_t=0
        attempts+=1
        result=""


def resetGame():
    global shot_active,shot_t,result,ball_x,ball_y
    global aim_x,score,attempts

    shot_active=False
    shot_t=0
    result=""
    ball_x,ball_y=450,110
    aim_x=450
    score=attempts=0


def keyboard(key,x,y):
    if key==b' ':
        shoot()
    elif key in (b'r',b'R'):
        resetGame()
    glutPostRedisplay()


def specialKeys(key,x,y):
    global aim_x

    if not shot_active and attempts < MAX_ATTEMPTS:
        if key==GLUT_KEY_LEFT:
            aim_x-=25
        elif key==GLUT_KEY_RIGHT:
            aim_x+=25
        aim_x=max(315,min(585,aim_x))

    glutPostRedisplay()


def update(value):
    global frame,keeper_x,shot_t,shot_active
    global ball_x,ball_y,result,score

    frame+=1
    keeper_x=450+85*math.sin(frame*.05)

    if shot_active:
        shot_t+=.025
        shot_t=min(shot_t,1)

        ball_x=450+(aim_x-450)*shot_t
        ball_y=110+320*shot_t+85*math.sin(math.pi*shot_t)

        if shot_t>=1:
            shot_active=False

            if abs(aim_x-keeper_x)<58:
                result="SAVED!"
            else:
                result="GOAL!"
                score+=1

            if attempts>=MAX_ATTEMPTS:
                result+=" GAME OVER!"

    glutPostRedisplay()
    glutTimerFunc(16,update,0)


def init():
    glClearColor(.1,.4,.2,1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,WIDTH,0,HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB)
    glutInitWindowSize(WIDTH,HEIGHT)
    glutInitWindowPosition(100,50)
    glutCreateWindow(b"Football Penalty Shootout Game")

    init()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialKeys)
    glutTimerFunc(0,update,0)
    glutMainLoop()


main()
