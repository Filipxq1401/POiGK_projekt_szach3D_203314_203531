import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import chess

import numpy as np

from imgui_bundle import imgui
from imgui_bundle.python_backends.pygame_backend import PygameRenderer

import pywavefront
import os

class Szachy():
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
        while running:

            for event in pygame.event.get():
                self.silnik_ui.impl.process_event(event)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            dt = clock.tick(60) / 1000.0
            kat += dt * 15
            self.silnik_ui.generuj_klatke()
            self.silnik_3d.generuj_klatke(kat)
            self.silnik_ui.renderuj_klatke()
            pygame.display.flip()

        self.silnik_ui.impl.shutdown()
        pygame.quit()

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
        

class model_3d():
    def __init__(self, nazwa):
        path = os.path.join("obj",nazwa)
        model = pywavefront.Wavefront(path, create_materials=True)
        self.material = list(model.materials.values())[0]
        self.wierzcholki = self.material.vertices
        self.tex_id = None
        if self.material.texture:
            path_tex = os.path.join("obj",self.material.texture.file_name)
            self.tex_id = self.load_tex(path_tex)

        self.kolor = self.material.diffuse if self.material.diffuse else [1, 1, 1]
        self.model_w_gpu = glGenLists(1)
        self.zapisz_do_gpu()

    def zapisz_do_gpu(self):
        glNewList(self.model_w_gpu, GL_COMPILE)

        if self.tex_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(self.kolor[0], self.kolor[1], self.kolor[2])
        glBegin(GL_TRIANGLES)
        v = self.wierzcholki
        for i in range(0, len(v), 8):
            glTexCoord2f(v[i], v[i+1])
            glNormal3f(v[i+2], v[i+3], v[i+4])
            glVertex3f(v[i+5], v[i+6], v[i+7])
        glEnd()

        glEndList()
    
    
    def load_tex(self, nazwa):
        tex = pygame.image.load(nazwa)
        tex_data = pygame.image.tobytes(tex, "RGBA", True)
        width, height = tex.get_size()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)
        return tex_id
    
    def rysuj(self):
        glCallList(self.model_w_gpu)

class Silnik_UI():
    def __init__(self,szer,wys):
        self.szerokosc = szer/4
        self.wysokosc = wys
        imgui.create_context()
        self.io = imgui.get_io()
        self.io.display_size = (szer,wys)
        self.impl = PygameRenderer()

    def generuj_klatke(self):
        self.impl.process_inputs()
        imgui.new_frame()
        flagi_okna = (
            imgui.WindowFlags_.no_move | 
            imgui.WindowFlags_.no_collapse | 
            imgui.WindowFlags_.no_resize |
            imgui.WindowFlags_.no_title_bar
        )
        imgui.set_next_window_pos((3*self.szerokosc,0), imgui.Cond_.always)
        imgui.set_next_window_size((self.szerokosc, self.wysokosc), imgui.Cond_.always)
        imgui.begin("Prawy panel", flags=flagi_okna)
        fps = imgui.get_io().framerate
        imgui.text(f"FPS: {fps:.1f}")
        imgui.end()

    def renderuj_klatke(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
        

if __name__ == "__main__":
    szachy = Szachy()
    szachy.start_gry()

