from OpenGL.GL import *
from OpenGL.GLU import *
import chess
import os

from czesc_3d.model_3d import model_3d

class Silnik_3D():
    def __init__(self, szer, wys):
        self.szerokosc = 3 * szer / 4
        self.wysokosc = wys
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.szerokosc / self.wysokosc), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(0.05, 0.15, 0.3, 1.0)
        
        # --------------------- Oświetlenie ---------------------
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        kolor_ambient = [0.25, 0.25, 0.25, 1.0]
        kolor_diffuse = [0.75, 0.75, 0.75, 1.0]
        kolor_specular = [0.4, 0.4, 0.4, 1.0]
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, kolor_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, kolor_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, kolor_specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 80.0)
        glShadeModel(GL_SMOOTH)
        # ----------------------------------------------------------------------

        self.szachownica = model_3d("10586_Chess Board_v2_Iterations-2.obj", centruj=False)

        self.aktualny_kat = 0
        
        pliki_figur = {
            chess.PAWN:   "Pawn.obj",
            chess.ROOK:   "Rook.obj",
            chess.KNIGHT: "Knight.obj",
            chess.BISHOP: "Bishop.obj",
            chess.QUEEN:  "Queen.obj",
            chess.KING:   "King.obj"
        }
        
        # Wczytywanie texutur figur (możliwe że nie wchodze całe, będzie trzeba pobrać orginalengo dla każdej figury)
        self.modele_figur = {}
        for typ_figury, nazwa_pliku in pliki_figur.items():
            self.modele_figur[(typ_figury, chess.WHITE)] = model_3d(nazwa_pliku, tekstura="białe_piony.jpg")
            self.modele_figur[(typ_figury, chess.BLACK)] = model_3d(nazwa_pliku, tekstura="Czarne_piony.jpg")
        
    def generuj_klatke(self, plansza, dt):
        glViewport(0, 0, int(self.szerokosc), int(self.wysokosc))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glEnable(GL_TEXTURE_2D)
        glLoadIdentity()
        glTranslatef(0.0, 0, -30.0)
        glRotatef(-50, 1, 0, 0)
        
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 12.0, 15.0, 1.0])

        # --- Obrót kamery ---
        cel_kat = 0.0 if plansza.turn else 180.0
        roznica = cel_kat - self.aktualny_kat
        predkosc = 180.0 
        
        if roznica != 0:
            krok = predkosc * dt
            if abs(roznica) <= krok:
                self.aktualny_kat = cel_kat
            else:
                self.aktualny_kat += krok if roznica > 0 else -krok
        
        glRotatef(self.aktualny_kat, 0, 0, 1)
        # --------------------------------------
        
        glPushMatrix()
        glScalef(0.446, 0.446, 0.446)
        self.szachownica.rysuj()
        glPopMatrix()
        
        glDisable(GL_TEXTURE_2D)  
        
        # ---------------------------- Wyświetlanie figur ----------------------------------------
        for i in range(0, 8):
            for j in range(0, 8):
                square = chess.square(j, i)
                figura = plansza.piece_at(square)
                
                if figura is not None:
                    glPushMatrix()
                    glTranslatef(-7.05 + 2 * j, -7.0 + 2 * i, 0.9)
                    
                    model = self.modele_figur.get((figura.piece_type, figura.color))
                    
                    if model:
                        glScalef(0.3, 0.3, 0.3) 
                        if figura.color == chess.WHITE:
                            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])
                        else:
                            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.05, 0.05, 0.05, 1.0])
                        
                        model.rysuj()
                    glPopMatrix()