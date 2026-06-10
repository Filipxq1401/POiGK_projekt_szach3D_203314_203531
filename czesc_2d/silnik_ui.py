from imgui_bundle import imgui
from imgui_bundle.python_backends.pygame_backend import PygameRenderer
import chess
import pygame
class Silnik_UI():
    def __init__(self, szer, wys):
        self.szerokosc = szer / 4
        self.wysokosc = wys
        imgui.create_context()
        self.io = imgui.get_io()
        self.io.display_size = (szer, wys)
        self.impl = PygameRenderer()

        self.czas_poczatkowy = 300
        self.czas_za_ruch = 0
        self.plik_partii = "przyklad.pgn"
        self.opoznienie_odtwarzania = 2
        self.font = self.io.fonts.add_font_from_file_ttf("C:/Windows/Fonts/arial.ttf", 10)
        self.pole_1 = ""
        self.pole_2 = ""
        self.udany_ruch = True
    
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

    def wyswietl_przyciski_dolne(self, gra):
        wysokosc_przyciskow = 55
        imgui.set_cursor_pos_y(self.wysokosc - wysokosc_przyciskow)
        imgui.separator()
        
        szer = (self.szerokosc - 20 - imgui.get_style().item_spacing.x * 2) / 3
        
        if imgui.button("Reset", imgui.ImVec2(szer, 35)):
            gra.reset_gry()
        imgui.same_line()
        if imgui.button("Cofnij", imgui.ImVec2(szer, 35)):
            gra.cofnij()
        imgui.same_line()
        if imgui.button("Wyjdz", imgui.ImVec2(szer, 35)):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

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

        if text == "00:00":
            imgui.text_colored((1.0, 0.0, 0.0, 1.0), text)
        else:
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

        if text == "00:00":
            imgui.text_colored((1.0, 0.0, 0.0, 1.0), text)
        else:
            if not tura_bialych:
                imgui.text_colored((0.0, 1.0, 0.0, 1.0), text)
            else:
                imgui.text_colored((0.7, 0.7, 0.7, 1.0), text)

        imgui.pop_font()
        imgui.end_child()
        imgui.pop_style_color()

        imgui.columns(1)
        imgui.end_child()

    
    def wyswietl_historie(self, historia):
        imgui.separator()
        imgui.push_font(self.font, 14)
        imgui.text("Ostatnie ruchy:")
        imgui.pop_font()
        
        imgui.push_font(self.font, 13)
        imgui.columns(3, "historia_cols", True)
        imgui.text("Tura")
        imgui.next_column()
        imgui.text("Kolor")
        imgui.next_column()
        imgui.text("Ruch")
        imgui.next_column()
        imgui.separator()
        
        for ruch, tura_bialych, numer in reversed(historia):
            imgui.text(str(numer // 2 + 1))
            imgui.next_column()
            imgui.text("Biale" if tura_bialych else "Czarne")
            imgui.next_column()
            imgui.text(str(ruch))
            imgui.next_column()
        
        imgui.columns(1)
        imgui.pop_font()

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
            gra.zacznij_normalne(self.czas_poczatkowy,self.czas_za_ruch)

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

    def wyswietl_menu_konca(self,outcome, wygrany):
        imgui.separator()
        imgui.push_font(self.font,30)
        tekst = "Koniec Gry"
        tekst_szerokosc = imgui.calc_text_size(tekst).x
        imgui.set_cursor_pos_x((self.szerokosc - tekst_szerokosc) / 2)
        imgui.text(tekst)
        imgui.pop_font()
        imgui.separator()
        imgui.push_font(self.font,20)
        if outcome is not None:
            tekst = ""
            tekst += outcome.result()
            tekst += " - "
            if outcome.winner is None:
                tekst += "remis"
            elif outcome.winner:
                tekst += "wygral gracz grajacy bialymi figurami"
            else:
                tekst += "wygral gracz grajacy czarnymi figurami"
        else:
            if wygrany:
                tekst = "1-0 - wygral gracz grajacy bialymi figurami"
            else:
                tekst = "0-1 - wygral gracz grajacy czarnymi figurami"
        tekst_szerokosc = imgui.calc_text_size(tekst).x
        imgui.set_cursor_pos_x((self.szerokosc - tekst_szerokosc) / 2)
        imgui.text(tekst)
        tekst = "Powod: "
        if outcome is None:
            tekst+="przeciwnikowi skonczyl sie czas"
        else:
            #print(outcome.termination)
            match outcome.termination:
                case chess.Termination.CHECKMATE:
                    tekst+="mat"
                case chess.Termination.STALEMATE:
                    tekst+="pat"
                case chess.Termination.INSUFFICIENT_MATERIAL:
                    tekst+="niewystarczajacy material do mata"
                case chess.Termination.SEVENTYFIVE_MOVES:
                    tekst+="zasada 75 ruchów"
                case chess.Termination.FIVEFOLD_REPETITION:
                    tekst+="pieciokrotne powtorzenie pozycji"
                case chess.Termination.FIFTY_MOVES:
                    tekst+="zasada 50 ruchów"
                case chess.Termination.THREEFOLD_REPETITION:
                    tekst+="trzykrotne powtorzenie pozycji"
        tekst_szerokosc = imgui.calc_text_size(tekst).x
        imgui.set_cursor_pos_x((self.szerokosc - tekst_szerokosc) / 2)
        imgui.text(tekst)  
        imgui.pop_font()
        imgui.spacing()
        przycisk = False
        imgui.set_cursor_pos_x((self.szerokosc - 180) / 2)
        if imgui.button("Resetuj gre", imgui.ImVec2(180, 35)):
            przycisk = True
        imgui.spacing()
        return przycisk
    
    def wyswietl_kontrolki(self,gra):
        imgui.separator()
        tekst = "Manualne wpisywanie ruchu"
        imgui.push_font(self.font,20)
        tekst_szerokosc = imgui.calc_text_size(tekst).x
        imgui.set_cursor_pos_x((self.szerokosc - tekst_szerokosc) / 2)
        imgui.text(tekst)
        imgui.pop_font()
        imgui.separator()
        imgui.text(" ")
        imgui.same_line()
        imgui.text("Pole figury: ")
        imgui.same_line()
        imgui.set_next_item_width(self.szerokosc * 0.2)
        zmieniono, watrosc = imgui.input_text("##pole_1",self.pole_1)
        try:
            if zmieniono:
                if len(watrosc) == 1:
                    if 'a' <= watrosc[0].lower() <= 'h':
                        self.pole_1 = watrosc
                elif len(watrosc) == 2:
                    if 'a' <= watrosc[0].lower() <= 'h' and 1 <= int(watrosc[1]) <= 8:
                        self.pole_1 = watrosc
                elif len(watrosc) == 0:
                    self.pole_1 = watrosc
        except:
            pass
        imgui.same_line()
        imgui.text("Pole docelowe: ")
        imgui.same_line()
        imgui.set_next_item_width(self.szerokosc * 0.2)
        zmieniono, watrosc = imgui.input_text("##pole_2",self.pole_2)
        try:
            if len(watrosc) == 1:
                if 'a' <= watrosc[0].lower() <= 'h':
                    self.pole_2 = watrosc
            elif len(watrosc) == 2:
                if 'a' <= watrosc[0].lower() <= 'h' and 1 <= int(watrosc[1]) <= 8:
                    self.pole_2 = watrosc
            elif len(watrosc) == 0:
                self.pole_2 = watrosc
        except:
            pass

        #imgui.spacing()
        imgui.same_line()
        #imgui.set_cursor_pos_x((self.szerokosc * 0.5 - przycisk_szerokosc) / 2)
        if imgui.button("Wykonaj ruch"):
            self.udany_ruch = gra.wykonaj_ruch_manualnie(self.pole_1,self.pole_2)
        #imgui.same_line()
        #imgui.set_cursor_pos_x((self.szerokosc * 0.5 - przycisk_szerokosc) / 2 + 0.5 * self.szerokosc)
        #if imgui.button("Cofnij ruch",imgui.ImVec2(przycisk_szerokosc, przycisk_wysokosc)):
        #    gra.cofnij()
        if not self.udany_ruch:
            tekst = "Niepoprawny ruch!!!"
            tekst_szerokosc = imgui.calc_text_size(tekst).x
            imgui.set_cursor_pos_x((self.szerokosc - tekst_szerokosc) / 2)
            imgui.text_colored((1.0, 0.0, 0.0, 1.0),tekst)

        
    def resetu_ruch(self):
        self.pole_1 = ""
        self.pole_2 = ""
        self.udany_ruch = True

    def resetuj(self):
        self.czas_poczatkowy = 300
        self.czas_za_ruch = 0
        self.plik_partii = "przyklad.pgn"
        self.opoznienie_odtwarzania = 2
        self.pole_1 = ""
        self.pole_2 = ""
        self.udany_ruch = True
        

    def renderuj_klatke(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
        
