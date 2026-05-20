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
        self.ruch_gracza=""
        self.historia = []

    def generuj_klatke(self,kat,skala):
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
        imgui.text(f"kat: {kat:.4f}")
        imgui.text(f"skala: {skala:.4f}")
        
        imgui.separator() 
        zmieniono, self.ruch_gracza = imgui.input_text("##pole_ruchu", self.ruch_gracza)
        imgui.same_line()

        if imgui.button("Wykonaj"):
            self.wykonaj_ruch(self.tekst_ruchu)
            self.tekst_ruchu = ""

        imgui.end()

    def renderuj_klatke(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def wykonaj_ruch(self, wpisany_ruch):
        print(f"Wykonuję ruch: {wpisany_ruch}")