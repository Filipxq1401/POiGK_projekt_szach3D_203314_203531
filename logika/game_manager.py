import pygame
from pygame.locals import *
import copy
from collections import deque

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
        self.stan = StanProgramu.Menu_poczatkowe
        self.kat = 0
        self.czy_koniec = False
        self.svg_planszy = self.logika.get_svg_planszy(None)
        self.nowa_plansza = True
        self.poprzednie_podswietlane_pola = []
        self.czy_promocja = False
        self.historia = deque([])

    def reset_gry(self):
        self.logika = Logika_szachy()
        self.silnik_ui.resetuj()
        self.stan = StanProgramu.Menu_poczatkowe
        self.kat = 0
        self.czy_koniec = False
        self.svg_planszy = self.logika.get_svg_planszy(None)
        self.nowa_plansza = True
        self.poprzednie_podswietlane_pola = []
        self.czy_promocja = False
    
    def start_gry(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            kliknete_pole = None
            dt = clock.tick(60) / 1000.0 # czas ruchu kamery
            
            czy_koniec_czasu = self.logika.aktualizuj_czas(dt, self.stan == StanProgramu.Normalne)
            if czy_koniec_czasu:
                #print("Czas minął!")
                self.stan = StanProgramu.Koniec
                self.czy_koniec = True
            
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
            
            if self.logika.czy_cos_sie_rusza():
                self.stan = StanProgramu.Poruszanie_figury
            elif self.stan == StanProgramu.Poruszanie_figury:
                if not self.logika.czy_promocja():
                    self.stan = StanProgramu.Obracanie_kamery
                    self.zapisz_logike()
                    self.czy_koniec = self.logika.nowa_tura()
                    self.svg_planszy = self.logika.get_svg_planszy(None)
                    self.silnik_ui.resetu_ruch()
                    self.nowa_plansza = True
                else:
                    self.stan = StanProgramu.Menu_promocji
                    self.czy_promocja = False
            
            if self.czy_koniec:
                pola_do_podswietlenia = self.logika.podswietlenie_baza(None,True)
                self.svg_planszy = self.logika.get_svg_planszy(pola_do_podswietlenia)
                self.nowa_plansza = True
                self.stan = StanProgramu.Koniec
            
            if self.stan == StanProgramu.Menu_promocji and self.czy_promocja:
                self.stan = StanProgramu.Poruszanie_figury

            aktualne_pole = self.silnik_3d.znajdz_pole(pygame.mouse.get_pos()) # pole na którym jest myszka
            #pola_do_podswietlenia = self.logika.podswietlenie_ograniczone(aktualne_pole)
            pola_do_podswietlenia = []
            poruszajace = []
            self.silnik_ui.inicjalizuj_klatke()
            match self.stan:
                case StanProgramu.Normalne:
                    pola_do_podswietlenia = self.logika.przetworz_myszke(kliknete_pole,aktualne_pole)
                    if pola_do_podswietlenia[1:] != self.poprzednie_podswietlane_pola and aktualne_pole is not None:
                        self.svg_planszy = self.logika.get_svg_planszy(pola_do_podswietlenia[1:])
                        self.nowa_plansza = True
                case StanProgramu.Poruszanie_figury:
                    self.logika.porusz(dt)
                    poruszajace = self.logika.get_poruszajace_figury()
                    pola_do_podswietlenia = self.logika.podswietlenie_baza(None)
                case StanProgramu.Obracanie_kamery:
                    pola_do_podswietlenia = self.logika.podswietlenie_baza(None)
                    cel_kat = 0.0 if self.logika.tura else 180.0
                    roznica = cel_kat - self.kat
                    predkosc = 180.0 
                    if roznica != 0:
                        krok = predkosc * dt
                        if abs(roznica) <= krok:
                            self.kat = cel_kat
                        else:
                            self.kat += krok if roznica > 0 else -krok
                    else:
                        self.stan = StanProgramu.Normalne
            
            if self.nowa_plansza:
                self.silnik_3d.zaladuj_plansze(pygame.image.load(self.svg_planszy, namehint="board.png").convert_alpha())
            
            if self.stan != StanProgramu.Menu_poczatkowe:
                self.silnik_ui.wyswietl_plansze(self.silnik_3d.tex_planszy)
                czas_bialych, czas_czarnych = self.logika.get_czas_str()
                self.silnik_ui.wyswietl_zegary(czas_bialych, czas_czarnych, self.logika.tura)
                self.silnik_ui.wyswietl_historie(self.logika.get_historia())
                if self.stan == StanProgramu.Menu_promocji:
                    self.czy_promocja = self.silnik_ui.wyswietl_menu_promocji(self.logika)
                elif self.stan == StanProgramu.Koniec:
                    pola_do_podswietlenia = self.logika.podswietlenie_baza(None,True)
                    if self.silnik_ui.wyswietl_menu_konca(self.logika.plansza.outcome(claim_draw=True), True if self.logika.wynik == 1 else False):
                        self.reset_gry()
                else:
                    self.silnik_ui.wyswietl_kontrolki(self)
                self.silnik_ui.wyswietl_przyciski_dolne(self,czy_gra=True)  
                self.silnik_ui.zakoncz_okno()
            else:
                self.silnik_ui.wyswietl_menu_poczatkowe(self)
                self.silnik_ui.wyswietl_przyciski_dolne(self, czy_gra=False)  
                self.silnik_ui.zakoncz_okno()
            self.silnik_3d.ustaw_kamere_swiatlo(self.kat,dt)
            self.silnik_3d.wyswietl_plansze()
            if pola_do_podswietlenia:
                self.silnik_3d.podswietl_pola(pola_do_podswietlenia)
            self.silnik_3d.wyswietl_figur_plansza(self.logika.get_figury_na_planszy())
            if poruszajace:
                self.silnik_3d.wyswietl_poruszajace(poruszajace)
            zbite = self.logika.get_zbite()
            self.silnik_3d.wyswietl_zbite(zbite)
            
            self.silnik_ui.renderuj_klatke()
            

            if pola_do_podswietlenia and aktualne_pole:
                pola_do_podswietlenia.pop(0)
            self.poprzednie_podswietlane_pola = pola_do_podswietlenia
            self.nowa_plansza = False
            
            pygame.display.flip()

        self.silnik_ui.impl.shutdown()
        pygame.quit()

    def wykonaj_ruch_manualnie(self,pozycja_poczatkowa,pozycja_koncowa):
        if len(pozycja_poczatkowa) == 2 and len(pozycja_koncowa) == 2:
            return self.logika.wykonaj_manulany_ruch(pozycja_poczatkowa,pozycja_koncowa)
        else:
            return False
    
    def cofnij_ruch(self):
        pass

    def zacznij_normalne(self,czas,bonus):
        self.logika.ustaw_czas(czas,bonus)
        self.stan = StanProgramu.Normalne
        self.svg_planszy = self.logika.get_svg_planszy(None)
        self.silnik_3d.zaladuj_plansze(pygame.image.load(self.svg_planszy, namehint="board.png").convert_alpha())


    def zapisz_logike(self):
        self.historia.append(copy.deepcopy(self.logika))

    def cofnij(self):
        if self.historia:
            self.logika = self.historia.pop()
            

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
    Menu_poczatkowe = auto()
    