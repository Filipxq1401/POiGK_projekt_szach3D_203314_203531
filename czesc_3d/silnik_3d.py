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
        #self.modele_figur = {}
        #for typ_figury, nazwa_pliku in pliki_figur.items():
        #    self.modele_figur[(typ_figury, chess.WHITE)] = model_3d(nazwa_pliku, tekstura="białe_piony.jpg")
        #    self.modele_figur[(typ_figury, chess.BLACK)] = model_3d(nazwa_pliku, tekstura="Czarne_piony.jpg")
        
    
    def ustaw_kamere(self, tura, dt):
        glViewport(0, 0, int(self.szerokosc), int(self.wysokosc))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # --- Obrót kamery ---
        cel_kat = 0.0 if tura else 180.0
        roznica = cel_kat - self.aktualny_kat
        predkosc = 180.0 
        
        if roznica != 0:
            krok = predkosc * dt
            if abs(roznica) <= krok:
                self.aktualny_kat = cel_kat
            else:
                self.aktualny_kat += krok if roznica > 0 else -krok

        kamera_x = 0.0
        kamera_y = -30 * np.sin(np.deg2rad(50))
        kamera_z = 30 * np.cos(np.deg2rad(50))
        
        gluLookAt(kamera_x, kamera_y, kamera_z,  0.0, 0.0, 1.0,  0.0, 0.0, 1.0)
        
        glRotatef(self.aktualny_kat, 0, 0, 1)
        self.model_mat = glGetDoublev(GL_MODELVIEW_MATRIX)

    def wyswietl_plansze(self):
        glPushMatrix()
        glScalef(0.446, 0.446, 0.446)
        self.szachownica.rysuj()
        glPopMatrix()
        
    def wyswietl_figur(self,plansza):
        # ---------------------------- Wyświetlanie figur ----------------------------------------
        #for i in range(0, 8):
        #    for j in range(0, 8):
        #        square = chess.square(j, i)
        #        figura = plansza.piece_at(square)
        #        
        #        if figura is not None:
        #            glPushMatrix()
        #            glTranslatef(-7.05 + 2 * j, -7.0 + 2 * i, 0.9)
        #            
        #            model = self.modele_figur.get((figura.piece_type, figura.color))
        #            
        #            if model:
        #                glScalef(0.3, 0.3, 0.3) 
        #                model.rysuj()
        #            glPopMatrix()
        pass

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