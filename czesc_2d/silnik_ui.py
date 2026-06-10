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

        self.czas_poczatkowy = 600
        self.czas_za_ruch = 0
        self.plik_partii = ""
        self.opoznienie_odtwarzania = 2
        self.font = self.io.fonts.add_font_from_file_ttf("C:/Windows/Fonts/arial.ttf", 10)
    
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
        imgui.push_font(self.font,15)

    def zakoncz_okno(self):
        imgui.pop_font()
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

    def wyswietl_menu_promocji(self, logika):
        imgui.separator()

        total = self.szerokosc - 20
        spacing = imgui.get_style().item_spacing.x
        szer = (total - spacing * 3) / 4

        if imgui.button("Hetman", imgui.ImVec2(szer, 40)):
            logika.wykonaj_promocje(0)
            return True
        imgui.same_line()

        if imgui.button("Wieża", imgui.ImVec2(szer, 40)):
            logika.wykonaj_promocje(1)
            return True
        imgui.same_line()

        if imgui.button("Goniec", imgui.ImVec2(szer, 40)):
            logika.wykonaj_promocje(2)
            return True
        imgui.same_line()

        if imgui.button("Skoczek", imgui.ImVec2(szer, 40)):
            logika.wykonaj_promocje(3)
            return True

        return False
    

    def wyswietl_menu_poczatkowe(self, gra):
        etykieta_szerokosc = 150
        input_szerokosc = 120
        przycisk_szerokosc = 180
        przycisk_wysokosc = 35

        imgui.separator()

        imgui.push_font(self.font,30)
        naglowek_1 = "Nowa gra"
        tekst_szerokosc_1 = imgui.calc_text_size(naglowek_1).x
        imgui.set_cursor_pos_x((self.szerokosc - tekst_szerokosc_1) / 2)
        imgui.text(naglowek_1)
        imgui.pop_font()

        imgui.separator()
        imgui.spacing()

        imgui.align_text_to_frame_padding()
        imgui.text("Czas poczatkowy (s):")
        imgui.same_line(etykieta_szerokosc)
        imgui.set_next_item_width(input_szerokosc)

        flaga = imgui.InputTextFlags_.chars_decimal

        _, self.czas_poczatkowy = imgui.input_text("##czas_pocz", str(self.czas_poczatkowy), flaga)
        try:
            self.czas_poczatkowy = max(0, int(self.czas_poczatkowy)) if self.czas_poczatkowy else 0
        except ValueError:
            self.czas_poczatkowy = 0

        imgui.align_text_to_frame_padding()
        imgui.text("Czas za ruch (s):")
        imgui.same_line(etykieta_szerokosc)
        imgui.set_next_item_width(input_szerokosc)

        _, self.czas_za_ruch = imgui.input_text("##czas_ruch", str(self.czas_za_ruch), flaga)
        try:
            self.czas_za_ruch = (max(0, int(self.czas_za_ruch)) if self.czas_za_ruch else 0)
        except ValueError:
            self.czas_za_ruch = 0

        imgui.spacing()

        imgui.set_cursor_pos_x((self.szerokosc - przycisk_szerokosc) / 2)
        if imgui.button("Zacznij gre", imgui.ImVec2(przycisk_szerokosc, przycisk_wysokosc)):
            gra.zacznij_normalne()

        imgui.spacing()

        imgui.separator()
        imgui.push_font(None,30)
        naglowek_2 = "Odtwarzanie partii"
        tekst_szerokosc_2 = imgui.calc_text_size(naglowek_2).x
        imgui.set_cursor_pos_x((self.szerokosc - tekst_szerokosc_2) / 2)
        imgui.text(naglowek_2)
        imgui.pop_font()

        imgui.separator()
        imgui.spacing()

        imgui.align_text_to_frame_padding()
        imgui.text("Plik partii (PGN):")
        imgui.same_line(etykieta_szerokosc)
        imgui.set_next_item_width(input_szerokosc + 60)
        _, self.plik_partii = imgui.input_text("##plik_partii", self.plik_partii)

        imgui.align_text_to_frame_padding()
        imgui.text("Opoznienie (s):")
        imgui.same_line(etykieta_szerokosc)
        imgui.set_next_item_width(input_szerokosc)


        _, self.opoznienie_odtwarzania = imgui.input_text("##opoznienie", str(self.opoznienie_odtwarzania), flaga)
        try:
            self.opoznienie_odtwarzania = max(0, float(self.opoznienie_odtwarzania)) if self.opoznienie_odtwarzania else 0
        except ValueError:
            self.opoznienie_odtwarzania = 0

        imgui.spacing()
        brak_pliku = self.plik_partii.strip() == ""
        imgui.set_cursor_pos_x((self.szerokosc - przycisk_szerokosc) / 2)

        imgui.begin_disabled(brak_pliku)
        if imgui.button("Odtwarzaj partie", imgui.ImVec2(przycisk_szerokosc, przycisk_wysokosc) ):
            gra.zacznij_odtwarzanie(self.plik_partii.strip(), self.opoznienie_odtwarzania)
        imgui.end_disabled()
        
        if brak_pliku:
            komunikat = "Podaj sciezke do pliku PGN"
            komunikat_szerokosc = imgui.calc_text_size(komunikat).x
            imgui.set_cursor_pos_x((self.szerokosc - komunikat_szerokosc) / 2)
            imgui.text_colored(imgui.ImVec4(1, 0.5, 0, 1), komunikat)
        

    def renderuj_klatke(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
