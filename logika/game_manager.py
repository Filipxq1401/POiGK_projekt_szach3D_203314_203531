import pygame
from pygame.locals import *


from czesc_3d.silnik_3d import Silnik_3D
from czesc_2d.silnik_ui import Silnik_UI

class Game_manager():
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.szerokosc = info.current_w
        self.wysokosc = info.current_h
        pygame.display.set_mode((self.szerokosc,self.wysokosc), DOUBLEBUF | OPENGL | NOFRAME)
        pygame.display.set_caption("Szachy 3D")
        self.silnik_3d = Silnik_3D(self.szerokosc,self.wysokosc)
        self.silnik_ui = Silnik_UI(self.szerokosc,self.wysokosc)


    def start_gry(self):
        clock = pygame.time.Clock()
        running = True
        kat = 0
        skala = 0.5
        while running:
            dt = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.silnik_ui.impl.process_event(event)
                
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                kat += dt * 15
            if keys[pygame.K_LEFT]:
                kat -= dt * 15
            if keys[pygame.K_UP]:
                skala += dt * 0.1
            if keys[pygame.K_DOWN]:
                skala -= dt * 0.1
            self.silnik_ui.generuj_klatke(kat,skala)
            self.silnik_3d.generuj_klatke(kat,skala)
            self.silnik_ui.renderuj_klatke()
            pygame.display.flip()

        self.silnik_ui.impl.shutdown()
        pygame.quit()