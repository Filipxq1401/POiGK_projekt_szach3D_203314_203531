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


    def start_gry(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(100) / 1000.0
            for event in pygame.event.get():
                self.silnik_ui.impl.process_event(event)
                
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            keys = pygame.key.get_pressed()
            self.silnik_ui.generuj_klatke(self)
            self.silnik_3d.generuj_klatke(self.logika.plansza)
            self.silnik_ui.renderuj_klatke()
            pygame.display.flip()

        self.silnik_ui.impl.shutdown()
        pygame.quit()

    def wykonaj_ruch(self,ruch):
        # tu jeszcze będzie zarządzanie animacjami ruchu i pozycjami poszczególnych figur
        return self.logika.wykonaj_ruch(ruch)
    
    def cofnij_ruch(self):
        self.logika.cofnij_ruch()