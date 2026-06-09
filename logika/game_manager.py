import pygame
from pygame.locals import *


from czesc_3d.silnik_3d import Silnik_3D
from czesc_2d.silnik_ui import Silnik_UI
from logika.logika_szachy import Logika_szachy


class Game_manager():
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.szerokosc = info.current_w
        self.wysokosc = info.current_h
        pygame.display.set_mode((self.szerokosc,self.wysokosc), DOUBLEBUF | OPENGL | NOFRAME)
        pygame.display.set_caption("Szachy 3D")
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        self.silnik_3d = Silnik_3D(self.szerokosc,self.wysokosc)
        self.silnik_ui = Silnik_UI(self.szerokosc,self.wysokosc)
        self.logika = Logika_szachy()
        self.stan = StanProgramu.Normalne


    def start_gry(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            kliknete_pole = None
            dt = clock.tick(120) / 1000.0 # czas ruchu kamery
            #----------------- Obsługa eventów -----------------
            for event in pygame.event.get():
                self.silnik_ui.impl.process_event(event)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                       kliknete_pole = self.silnik_3d.znajdz_pole(event.pos)
            
            match self.stan:
                case StanProgramu.Normalne:
                    aktualne_pole = self.silnik_3d.znajdz_pole(pygame.mouse.get_pos()) # pole na którym jest myszka
                    pola_do_podswietlenia = self.logika.przetworz_myszke(kliknete_pole,aktualne_pole)
                    plansza = self.logika.get_plansza()
                    plansza_str = ""
                    for i in range(8):
                        for j in range(8):
                            kolumna = j
                            wiersz = 7 - i
                            pozycja = 10*wiersz+kolumna
                            if pola_do_podswietlenia:
                                tak = True
                                for pole in pola_do_podswietlenia:
                                    if pole[0] == pozycja:
                                        plansza_str += "-" + str(plansza[kolumna][wiersz])[0] + "-"
                                        tak = False
                                        break
                                if tak:
                                    plansza_str += " " + str(plansza[kolumna][wiersz])[0] + " "
                            else:
                                plansza_str += " " + str(plansza[kolumna][wiersz])[0] + " "
                        plansza_str += "\n" 
                    self.silnik_ui.generuj_klatke(self,self.logika.plansza,plansza_str)

                    self.silnik_3d.ustaw_kamere(self.logika.plansza.turn,dt)
                    self.silnik_3d.wyswietl_plansze()
                    self.silnik_3d.podswietl_pola(pola_do_podswietlenia)
                    self.silnik_3d.wyswietl_figur_plansza(self.logika.get_figury_na_planszy())

                    self.silnik_ui.renderuj_klatke()
            
            
            pygame.display.flip()

        self.silnik_ui.impl.shutdown()
        pygame.quit()

    def wykonaj_ruch(self,ruch):
        # tu jeszcze będzie zarządzanie animacjami ruchu i pozycjami poszczególnych figur
        return self.logika.wykonaj_ruch(ruch)
    
    def cofnij_ruch(self):
        self.logika.cofnij_ruch()

#init 
#jak się klikne na figure to sprawdza legalność ruchów
#jak się zrobi ruch to wtedy sprawdza się czy przeciwnik jest w szachu i czy ma dostepne ruchy
# w szachu i brak legalnych ruchów -> koniec gry, wygrywa gracz który zrobił ruch
# nie w szachi i brak legalnych ruchów -> koniec gry, remis
# można iść dalej
from enum import Enum, auto

class StanProgramu(Enum):
    Normalne = auto()
    Poruszanie_figury = auto()
    Menu_promocji = auto()
    Obracanie_kamery = auto()
    Koniec = auto()
    