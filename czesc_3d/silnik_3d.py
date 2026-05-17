from OpenGL.GL import *
from OpenGL.GLU import *

from model_3d import model_3d

class Silnik_3D():
    def __init__(self,szer,wys):
        self.szerokosc = 3*szer/4
        self.wysokosc = wys
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.szerokosc / self.wysokosc), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        self.szachownica = model_3d("10586_Chess Board_v2_Iterations-2.obj")
        
    
    def generuj_klatke(self,kat):
        glViewport(0,0,int(self.szerokosc),int(self.wysokosc))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0, -15.0)
        glRotatef(-60, 1, 0, 0)
        glScale(0.2,0.2,0.2)
        glRotatef(kat,0,0,1)
        self.szachownica.rysuj()