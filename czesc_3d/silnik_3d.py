from OpenGL.GL import *
from OpenGL.GLU import *
import chess
import os
import numpy as np
from czesc_3d.model_3d import model_3d

class Silnik_3D():
    def __init__(self, szer, wys):
        self.szerokosc = 3 * szer / 4
        self.wysokosc = wys
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.szerokosc / self.wysokosc), 0.1, 50.0)
        self.proj_mat = glGetDoublev(GL_PROJECTION_MATRIX)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(0.05, 0.15, 0.3, 1.0)
        self.model_mat = None
        self.szachownica = model_3d("10586_Chess Board_v2_Iterations-2.obj", centruj=True)

        
        pliki_figur = {
            chess.PAWN:   "Pawn.obj",
            chess.ROOK:   "Rook.obj",
            chess.KNIGHT: "Knight.obj",
            chess.BISHOP: "Bishop.obj",
            chess.QUEEN:  "Queen.obj",
            chess.KING:   "King.obj"
        }
        
        # Wczytywanie texutur figur (możliwe że nie wchodze całe, będzie trzeba pobrać orginalengo dla każdej figury)
        #self.modele_figur = {}
        #for typ_figury, nazwa_pliku in pliki_figur.items():
        #    self.modele_figur[(typ_figury, chess.WHITE)] = model_3d(nazwa_pliku, tekstura="białe_piony.jpg")
        #    self.modele_figur[(typ_figury, chess.BLACK)] = model_3d(nazwa_pliku, tekstura="Czarne_piony.jpg")
        
    
    def ustaw_kamere(self, kat, dt):
        glViewport(0, 0, int(self.szerokosc), int(self.wysokosc))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        kat

        kamera_x = 0.0
        kamera_y = -30 * np.sin(np.deg2rad(50))
        kamera_z = 30 * np.cos(np.deg2rad(50))
        
        gluLookAt(kamera_x, kamera_y, kamera_z,  0.0, 0.0, 1.0,  0.0, 0.0, 1.0)
        
        glRotatef(kat, 0, 0, 1)
        self.model_mat = glGetDoublev(GL_MODELVIEW_MATRIX)

    def wyswietl_plansze(self):
        glPushMatrix()
        glScalef(0.446, 0.446, 0.446)
        self.szachownica.rysuj()
        glPopMatrix()
        
    def wyswietl_figur_plansza(self,figury):
        for figura in figury:
            pozycja = figura.get_pozycja()
            wiersz = pozycja // 10
            kolumna = pozycja % 10
            glPushMatrix()
            glTranslatef(-7 + 2*kolumna,-7 + 2*wiersz,1)
            glScalef(0.3, 0.3, 0.3) 
            if figura.model_czarny is None or figura.model_bialy is None:
                print(figura)
            else:
                figura.wyswietl()
            glPopMatrix()
    
    def wyswietl_poruszajace(self,figury):
        for figura in figury:
            if figura:
                x,y,z = figura.xyz_aktualne
                glPushMatrix()
                glTranslatef(x,y,1)
                glScalef(0.3, 0.3, 0.3)
                figura.wyswietl()
                glPopMatrix()

    def znajdz_pole(self, pozycja):
        x ,y = pozycja
        if x >= self.szerokosc:
            return None
            
        x_przeliczone = x 
        y_przeliczone = self.wysokosc - y
        
        viewport = glGetIntegerv(GL_VIEWPORT)

        punkt_near = np.array(gluUnProject(x_przeliczone, y_przeliczone, 0.0, self.model_mat, self.proj_mat, viewport))
        punkt_far = np.array(gluUnProject(x_przeliczone, y_przeliczone, 1.0, self.model_mat, self.proj_mat, viewport))
        kierunek = punkt_far - punkt_near
        

        if abs(kierunek[2]) < 0.0001: # aby nie dzielić przez zero
            return None
            
        t = (1 - punkt_near[2]) / kierunek[2] # przecięcie z szachownicą
        
        punkt_uderzenia = punkt_near + t * kierunek
        uderzenie_x = punkt_uderzenia[0]
        uderzenie_y = punkt_uderzenia[1] 
        
        #print(f"x={uderzenie_x:.2f}, y={uderzenie_y:.2f}")
        
        wiersz = int((uderzenie_y + 8) // 2)
        kolumna = int((uderzenie_x + 8) // 2)

        if 0<= wiersz <=7 and 0<= kolumna <=7:
            return 10*wiersz + kolumna
        
        return
    
    def podswietl_pola(self,pola):
        for pole in pola:
            pozycja = pole[0]
            R,G,B = pole[1:4]
            wiersz = pozycja // 10
            kolumna = pozycja % 10
            glPushMatrix()
            glScalef(1,1,0.5)
            glTranslatef(-7 + 2*kolumna,-7 + 2*wiersz,1)
            wyswietl_szescian([R,G,B,0.5])
            glPopMatrix()



def wyswietl_szescian(kolor):
    wierzcholki = [
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (1, -1, -1),
        (-1, 1, 1),
        (-1, 1, -1),
        (-1, -1, 1),
        (-1, -1, -1)]
    sciany = [
        (0, 1, 3, 2),
        (4, 5, 7, 6),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 2, 6, 4),
        (1, 3, 7, 5)
    ]
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glColor4fv(kolor)
    for sciana in sciany:
        for wierzholek in sciana:
            glVertex3fv(wierzcholki[wierzholek])
    glEnd()
    