from imgui_bundle import imgui
from imgui_bundle.python_backends.pygame_backend import PygameRenderer

class Silnik_UI():
    def __init__(self,szer,wys):
        self.szerokosc = szer/4
        self.wysokosc = wys
        imgui.create_context()
        self.io = imgui.get_io()
        self.io.display_size = (szer,wys)
        self.impl = PygameRenderer()
        self.ruch=""
        self.blad = False

    def generuj_klatke(self,game_manager):
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
        
        imgui.separator() 
        zmieniono, self.ruch = imgui.input_text("##pole_ruchu", self.ruch)
        imgui.same_line()

        if imgui.button("Wykonaj"):
            if not game_manager.wykonaj_ruch(self.ruch):
                self.blad = True
            else:
                self.blad = False
            self.ruch = ""
        if self.blad:
            imgui.text_colored([255,0,0,1],"Nieprawidlowy ruch")
        imgui.end()

    def renderuj_klatke(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
