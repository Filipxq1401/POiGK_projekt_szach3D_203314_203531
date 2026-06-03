from OpenGL.GL import *
from OpenGL.GLU import *
import chess
import os

from czesc_3d.model_3d import model_3d

class Silnik_3D():
    def __init__(self, szer, wys):
        self.szerokosc = 3 * szer / 4
        self.wysokosc = wys
        
        # Konfiguracja rzutowania i sceny
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.szerokosc / self.wysokosc), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(0.05, 0.15, 0.3, 1.0)
        
        # Wczytanie modelu szachownicy 
        self.szachownica = model_3d("10586_Chess Board_v2_Iterations-2.obj")

        self.aktualny_kat = 0
        
        # Ustawianie koloru
        kolor_bialy = [0.9, 0.9, 0.8]      
        kolor_czarny = [0.15, 0.15, 0.15]  
        
        # Pliki figur
        pliki_figur = {
            chess.PAWN: "Pawn.stl",
            chess.ROOK: "Rook.stl",
            chess.KNIGHT: "Knight.stl",
            chess.BISHOP: "Bishop.stl",
            chess.QUEEN: "Queen.stl",
            chess.KING: "King.stl"
        }
        
        # Wczytanie modeli dla białych i czarnych
        self.modele_figur = {}
        for typ_figury, nazwa_pliku in pliki_figur.items():
            self.modele_figur[(typ_figury, chess.WHITE)] = model_3d(nazwa_pliku, kolor_piona=kolor_bialy)
            self.modele_figur[(typ_figury, chess.BLACK)] = model_3d(nazwa_pliku, kolor_piona=kolor_czarny)
        
    def generuj_klatke(self, plansza, dt):
        glViewport(0, 0, int(self.szerokosc), int(self.wysokosc))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glEnable(GL_TEXTURE_2D)
        glLoadIdentity()
        glTranslatef(0.0, 0, -30.0)
        glRotatef(-50, 1, 0, 0)
        
        # ---  Obrót kamery ---
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
                figura = plansza.piece_at(square)  # Pobranie figury z danego pola
                
                if figura is not None:
                    glPushMatrix()
                    glTranslatef(-7.05 + 2 * j, -7.0 + 2 * i, 0.9)
                    
                    # Pobranie modelu na podstawie (Typ Figury, Kolor)
                    model = self.modele_figur.get((figura.piece_type, figura.color))
                    
                    if model:
                        glScalef(0.05, 0.05, 0.05) # Zmiana rozmiaru

                        if figura.piece_type == chess.KNIGHT: # Kierunek konia
                            if figura.color == chess.WHITE:
                                glRotatef(90, 0, 0, 1)    
                            else:
                                glRotatef(-90, 0, 0, 1)
                        
                        model.rysuj()
                    glPopMatrix()
        # ------------------------------------------------------------------------------------------