import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import os

class model_3d():
    def __init__(self, nazwa, kolor_piona=[0.7,0.7,0.7], tekstura=None, centruj=True, tekstura_id=None, 
             specular=[0.9, 0.9, 0.9, 1.0],  # Z [0.2, 0.2, 0.2, 1.0] -> jasny, wyraźny błysk
             shininess=80.0,                 # Z 16.0 -> ostrzejszy, skupiony punkt światła
             ambient_factor=0.25):
        path = os.path.join("czesc_3d/obj", nazwa) 
        
        self.tex_id = None
        self.model_w_gpu = glGenLists(1)
        self.specular = specular
        self.shininess = shininess
        self.ambient_factor = ambient_factor
        model = pywavefront.Wavefront(path, create_materials=True)
        self.material = list(model.materials.values())[0]
        self.wierzcholki = list(self.material.vertices) 
        
        # --- centorowanie modelu ---
        if centruj and self.wierzcholki:
            x_coords = [self.wierzcholki[i+5] for i in range(0, len(self.wierzcholki), 8)]
            y_coords = [self.wierzcholki[i+6] for i in range(0, len(self.wierzcholki), 8)]
            z_coords = [self.wierzcholki[i+7] for i in range(0, len(self.wierzcholki), 8)]
            
            # Szukanie środka
            srodek_x = (min(x_coords) + max(x_coords)) / 2
            srodek_y = (min(y_coords) + max(y_coords)) / 2
            najnizszy_z = min(z_coords) # Spód figury
            
            # Środkowanie figur
            for i in range(0, len(self.wierzcholki), 8):
                self.wierzcholki[i+5] -= srodek_x
                self.wierzcholki[i+6] -= srodek_y
                self.wierzcholki[i+7] -= najnizszy_z
        # ----------------------------------------------------
        
        # Ładowanie tekstury
        if tekstura:
            path_tex = os.path.join("czesc_3d/obj", tekstura)
            if os.path.exists(path_tex):
                self.tex_id = self.load_tex(path_tex)
        elif self.material.texture:
            path_tex = os.path.join("czesc_3d/obj", self.material.texture.file_name)
            if os.path.exists(path_tex):
                self.tex_id = self.load_tex(path_tex)
        elif tekstura_id:
            self.tex_id = tekstura_id
        
        self.kolor = kolor_piona
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
    # Ustaw materiał
        ambient = [self.kolor[0] * self.ambient_factor, self.kolor[1] * self.ambient_factor, self.kolor[2] * self.ambient_factor, 1.0]
        diffuse = [self.kolor[0], self.kolor[1], self.kolor[2], 1.0]

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, self.shininess)

        if self.tex_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(self.kolor[0], self.kolor[1], self.kolor[2])

        glCallList(self.model_w_gpu)

        if self.tex_id:
            glBindTexture(GL_TEXTURE_2D, 0)