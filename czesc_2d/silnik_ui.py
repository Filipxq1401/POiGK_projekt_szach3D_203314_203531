from imgui_bundle import imgui
from imgui_bundle.python_backends.pygame_backend import PygameRenderer
class Silnik_UI():
    def __init__(self, szer, wys):
        self.szerokosc = szer / 4
        self.wysokosc = wys
        imgui.create_context()
        self.io = imgui.get_io()
        self.io.display_size = (szer, wys)
        self.impl = PygameRenderer()
        self.ruch=""
        self.blad = False
    
    def inicjalizuj_klatke(self):
        self.impl.process_inputs()
        imgui.new_frame()
        
        flagi_okna = (
            imgui.WindowFlags_.no_move | 
            imgui.WindowFlags_.no_collapse | 
            imgui.WindowFlags_.no_resize |
            imgui.WindowFlags_.no_title_bar
        )
        
        imgui.set_next_window_pos((3 * self.szerokosc, 0), imgui.Cond_.always)
        imgui.set_next_window_size((self.szerokosc, self.wysokosc), imgui.Cond_.always)
        
        imgui.begin("Prawy panel", flags=flagi_okna)

    def zakoncz_okno(self):
        imgui.end()

    def wyswietl_zegary(self, czas_bialych, czas_czarnych, tura_bialych):
        imgui.dummy(imgui.ImVec2(0, 15))
        imgui.begin_child("zegary_panel", imgui.ImVec2(self.szerokosc - 20, 70), False)
        imgui.columns(2, None, False)

        imgui.push_style_color(imgui.Col_.child_bg, (0.92, 0.92, 0.92, 1.0))
        imgui.begin_child("czas_bialych", imgui.ImVec2(0, 50), True)

        text = f"{czas_bialych}"
        imgui.push_font(None, 28)
        tw = imgui.calc_text_size(text).x
        ww = imgui.get_window_width()
        imgui.set_cursor_pos_x((ww - tw) / 2)

        if tura_bialych:
            imgui.text_colored((0.0, 1.0, 0.0, 1.0), text)
        else:
            imgui.text_colored((0.4, 0.4, 0.4, 1.0), text)

        imgui.pop_font()
        imgui.end_child()
        imgui.pop_style_color()

        imgui.next_column()

        imgui.push_style_color(imgui.Col_.child_bg, (0.1, 0.1, 0.1, 1.0))
        imgui.begin_child("czas_czarnych", imgui.ImVec2(0, 50), True)

        text = f"{czas_czarnych}"
        imgui.push_font(None, 28)
        tw = imgui.calc_text_size(text).x
        ww = imgui.get_window_width()
        imgui.set_cursor_pos_x((ww - tw) / 2)

        if not tura_bialych:
            imgui.text_colored((0.0, 1.0, 0.0, 1.0), text)
        else:
            imgui.text_colored((0.7, 0.7, 0.7, 1.0), text)

        imgui.pop_font()
        imgui.end_child()
        imgui.pop_style_color()

        imgui.columns(1)
        imgui.end_child()


    def wyswietl_plansze(self,plansza):
        imgui.image(imgui.ImTextureRef(plansza),imgui.ImVec2(self.szerokosc - 10,self.szerokosc - 10))

    def wyswietl_menu_promocji(self,logika):
        imgui.separator()
        if imgui.button("Hetman"):
            logika.wykonaj_promocje(0)
            return True
        imgui.same_line()
        if imgui.button("Wieza"):
            logika.wykonaj_promocje(1)
            return True
        imgui.same_line()
        if imgui.button("Goniec"):
            logika.wykonaj_promocje(2)
            return True
        imgui.same_line()
        if imgui.button("Skoczek"):
            logika.wykonaj_promocje(3)
            return True
        return False

    def renderuj_klatke(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
