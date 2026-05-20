from OpenGL.GL import *
from OpenGL.GLU import *
import chess

from czesc_3d.model_3d import model_3d

class Silnik_3D():
    def __init__(self,szer,wys):
        self.szerokosc = 3*szer/4
        self.wysokosc = wys
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.szerokosc / self.wysokosc), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(0.05, 0.15, 0.3, 1.0)
        self.szachownica = model_3d("10586_Chess Board_v2_Iterations-2.obj")
        
    
    def generuj_klatke(self,plansza):
        glViewport(0,0,int(self.szerokosc),int(self.wysokosc))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        glLoadIdentity()
        glTranslatef(0.0, 0, -30.0)
        glRotatef(-50, 1, 0, 0)
        kat = 0 if plansza.turn else 180
        glRotatef(kat,0,0,1)
        glPushMatrix()
        glScalef(0.446,0.446,0.446)
        self.szachownica.rysuj()
        glPopMatrix()
        # Szachownica ma w Z 2 i po 10 w X i Y, 
        glDisable(GL_TEXTURE_2D)
        #glLoadIdentity()
        #glTranslatef(0.0, 0, -35.0)
        #glRotatef(-60, 1, 0, 0)
        #glRotatef(kat,0,1,0)
        #glTranslatef(-8,-8,1)
        glScalef(1,1,3)
        glColor3f(1,1,1)
        for i in range(0,8):
            for j in range(0,8):
                square = chess.square(i,j)
                if i < 2 or i > 5:
                    glPushMatrix()
                    glTranslatef(-7.5+2*j,-7.5+2*i,0)
                    draw_cube()
                    glPopMatrix()
                if i == 3:
                    glColor3f(0,0,0)

cube_vertices = (
    (1, 1, 1),    # 0: prawy-górny-przód
    (1, 1, 0),   # 1: prawy-górny-tył
    (1, 0, 1),   # 2: prawy-dolny-przód
    (1, 0, 0),  # 3: prawy-dolny-tył
    (0, 1, 1),   # 4: lewy-górny-przód
    (0, 1, 0),  # 5: lewy-górny-tył
    (0, 0, 1),  # 6: lewy-dolny-przód
    (0, 0, 0)  # 7: lewy-dolny-tył
)
def draw_cube():
    faces = (
        (0, 1, 3, 2),  # prawa ściana
        (4, 5, 7, 6),  # lewa ściana
        (0, 1, 5, 4),  # górna ściana
        (2, 3, 7, 6),  # dolna ściana
        (0, 2, 6, 4),  # przednia ściana
        (1, 3, 7, 5)   # tylna ściana
    )
    
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        #glColor3fv((1,1,1))
        for vertex in face:
            glVertex3fv(cube_vertices[vertex])
    glEnd()


    