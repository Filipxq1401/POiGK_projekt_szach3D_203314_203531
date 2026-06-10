import chess
import chess.svg
from logika.figury import *
import copy
import io
import cairosvg
class Logika_szachy():
    def __init__(self):
        self.plansza = chess.Board()
        self.gracz_bialy = Gracz(True)
        self.gracz_czarny = Gracz(False)
        self.wybrana_figura = None
        self.legalne_ruchy_wybranej_figury = None
        self.plansza_wlasna = self.stworz_nowa_plansze()
        self.tura = True # tura białego
        self.numer_tury = 0 
        self.wynik = 0
        self.powod_remisu = 0
        self.pionek_do_promocji = None

    def wykonaj_ruch(self,ruch):
        try:
            move = self.plansza.parse_san(ruch)
        except:
            return False
        if self.plansza.is_legal(move):
            self.plansza.push(move)
            return True
        else:
            return False
        
    def cofnij_ruch(self):
        try:
            self.plansza.pop()
        except:
            pass

    def stworz_nowa_plansze(self):
        figury = self.gracz_bialy.get_figury_na_planszy() + self.gracz_czarny.get_figury_na_planszy()
        self.plansza_wlasna = [[None for _ in range(8)] for _ in range(8)]
        for figura in figury:
            pozycja = figura.get_pozycja()
            wiersz = pozycja // 10
            kolumna = pozycja % 10
            if wiersz in range(8) or kolumna in range(8):
                self.plansza_wlasna[kolumna][wiersz] = figura
        
        return self.plansza_wlasna
    
    def podswietlenie_baza(self,hover):
        pola_do_podświetlenia = []
        if hover is not None:
            pola_do_podświetlenia.append([hover, 0,1,0]) # czerwone
        if self.wybrana_figura:
            pola_do_podświetlenia.append([self.wybrana_figura.get_pozycja(),1,1,0])
        if self.gracz_bialy.czy_szach():
            pola_do_podświetlenia.append([self.gracz_bialy.pozycja_krola(),1,0,0])
        if self.gracz_czarny.czy_szach():
            pola_do_podświetlenia.append([self.gracz_czarny.pozycja_krola(),1,0,0])
       
        return pola_do_podświetlenia
    
    def przetworz_myszke(self,wybrane,hover):
        pola_do_podświetlenia = []
        pola_do_podświetlenia = self.podswietlenie_baza(hover)
        if len(pola_do_podświetlenia) == 0:
            pola_do_podświetlenia = []
        if wybrane is not None:
            kolumna = wybrane % 10
            wiersz = wybrane // 10
            if self.plansza_wlasna[kolumna][wiersz] and self.plansza_wlasna[kolumna][wiersz].get_kolor() == self.tura: # wybrana została dobra figura
                self.wybierz_figure(self.plansza_wlasna[kolumna][wiersz])
            else:
                if self.legalne_ruchy_wybranej_figury:
                    for ruch in self.legalne_ruchy_wybranej_figury:
                        if ruch[1] == wybrane:
                            self.rozpocznij_ruch_wlasny(ruch) # kliknęte było pole na które jest możliwość ruchu
                            return pola_do_podświetlenia
                self.wybierz_figure(None)
        if self.wybrana_figura:
            if self.legalne_ruchy_wybranej_figury:
                for ruch in self.legalne_ruchy_wybranej_figury:
                    pola_do_podświetlenia.append([ruch[1],0,0,1])
        return pola_do_podświetlenia
        
    def wybierz_figure(self,figura):
        if figura is None:
            self.wybrana_figura = None
            self.legalne_ruchy_wybranej_figury = None
            return
        self.wybrana_figura = figura
        pseudo_legalne = figura.ruchy_pseudo_legalne(self.plansza_wlasna)
        #print(figura)
        #print(pseudo_legalne)
        self.legalne_ruchy_wybranej_figury = []
        if pseudo_legalne:
            for ruch in pseudo_legalne:
                if self.sprawdz_czy_legalny(ruch):
                    self.legalne_ruchy_wybranej_figury.append(ruch)

    
    def sprawdz_czy_legalny(self, ruch):
        plansza_po_ruchu = copy.deepcopy(self.plansza_wlasna)
        plansza_po_ruchu[ruch[1]%10][ruch[1]//10] = plansza_po_ruchu[ruch[0]%10][ruch[0]//10]
        plansza_po_ruchu[ruch[0]%10][ruch[0]//10] = None
        # obsługa bicia w przelocie
        for figura in plansza_po_ruchu:
            if figura is not None and isinstance(figura,pionek):
                figura.czy_do_przelotu = False
        
        if isinstance(plansza_po_ruchu[ruch[1]%10][ruch[1]//10],pionek) and ruch[2] == "przelot":
            plansza_po_ruchu[ruch[1]%10][ruch[1]//10].czy_do_przelotu = False
            plansza_po_ruchu[ruch[1]%10][ruch[0]//10] = None

        if self.tura:
            pozycja_krola = self.gracz_bialy.pozycja_krola()
            figury = self.gracz_czarny.get_figury_na_planszy()
        else:
            pozycja_krola = self.gracz_czarny.pozycja_krola()
            figury = self.gracz_bialy.get_figury_na_planszy()
        
        pozycje_krola = []
        if pozycja_krola == ruch[0]: # jeżeli król się porusza
            pozycje_krola.append(ruch[1])
        else:
            pozycje_krola.append(pozycja_krola)
        if ruch[2] == "roszada_krotka":
            pozycje_krola.append(ruch[0])
            pozycje_krola.append(ruch[0]+1)
        if ruch[2] == "roszada_dluga":
            pozycje_krola.append(ruch[0])
            pozycje_krola.append(ruch[0]-1)
        for krol in pozycje_krola:
            plansza_po_ruchu[krol%10][krol//10] = plansza_po_ruchu[pozycje_krola[0]%10][pozycje_krola[0]//10]
        #print(pozycje_krola)
        for figura in figury:
            if figura.get_pozycja() != ruch[1]: # jeżeli ta figura nie ma być zbita tym ruchem
                ruchy_przeciwnika = figura.ruchy_pseudo_legalne(plansza_po_ruchu)
                if ruchy_przeciwnika:
                    for ruch_przeciwnika in ruchy_przeciwnika:
                        if ruch_przeciwnika[1] in pozycje_krola and ruch_przeciwnika[2] == "bicie":
                            #print(ruch_przeciwnika)
                            del plansza_po_ruchu
                            return False
        del plansza_po_ruchu
        return True

    def rozpocznij_ruch_wlasny(self,ruch):
        w_akt = ruch[0] // 10
        k_akt = ruch[0] % 10
        w_doc = ruch[1] // 10
        k_doc = ruch[1] % 10
        ruch_chess = chess.Move(chess.square(k_akt,w_akt),chess.square(k_doc,w_doc))
        if self.tura:
            self.gracz_bialy.rozpocznij_ruch(self.plansza_wlasna,ruch)
            self.gracz_czarny.rozpocznij_zbicie(self.plansza_wlasna,ruch)
        else:
            self.gracz_czarny.rozpocznij_ruch(self.plansza_wlasna,ruch)
            self.gracz_bialy.rozpocznij_zbicie(self.plansza_wlasna,ruch)
        #self.plansza_wlasna[k_akt][w_akt].porusz(ruch[1])
        #if ruch[2] == "bicie":
        #    self.plansza_wlasna[k_doc][w_doc].zbij()
        self.wykonaj_ruch(self.plansza.san(ruch_chess))
        self.wybierz_figure(None)

    def nowa_tura(self):
        self.plansza_wlasna = self.stworz_nowa_plansze()
        self.tura = not self.tura
        if self.tura:
            self.gracz_bialy.resetuj_przelot()
        else:
            self.gracz_czarny.resetuj_przelot()
        self.numer_tury += 1
        czy_jakis_ruch = self.czy_ma_ruchy()
        self.gracz_bialy.ustaw_szach(self.czy_szach(True))
        self.gracz_czarny.ustaw_szach(self.czy_szach(False))
        if not czy_jakis_ruch:
            if self.tura:
                if self.gracz_bialy.czy_szach():
                    self.wynik = 2
                    return True
                else:
                    self.wynik = 0
                    self.powod_remisu = 2
                    return True
            else:
                if self.gracz_czarny.czy_szach():
                    self.wynik = 1
                    return True
                else:
                    self.wynik = 0
                    self.powod_remisu = 2
                    return True
        else:
            wynik = self.plansza.outcome()
            if wynik:
                if wynik.result() == "1/2-1/2":
                    self.wynik = 0
                    self.powod_remisu = wynik.termination()
                elif wynik.result() == "1-0":
                    self.wynik = 1
                else:
                    self.wynik = 2
                return True
            else:
                return False

        

    def czy_szach(self,kolor):
        if kolor:
            pozycja_krola = self.gracz_bialy.pozycja_krola()
            figury = self.gracz_czarny.get_figury_na_planszy()
            gracz = self.gracz_bialy
        else:
            pozycja_krola = self.gracz_czarny.pozycja_krola()
            figury = self.gracz_bialy.get_figury_na_planszy()
            gracz = self.gracz_czarny
        for figura in figury:
            ruchy_przeciwnika = figura.ruchy_pseudo_legalne(self.plansza_wlasna)
            if ruchy_przeciwnika:
                for ruch_przeciwnika in ruchy_przeciwnika:
                    if ruch_przeciwnika[1] == pozycja_krola and ruch_przeciwnika[2] == "bicie":
                        gracz.ustaw_szach(True)
                        return True
        gracz.ustaw_szach(False)
        return False
    
    def czy_ma_ruchy(self):
        if self.tura:
            figury = self.gracz_bialy.get_figury_na_planszy()
        else:
            figury = self.gracz_czarny.get_figury_na_planszy()
        for figura in figury:
            pseudo_legalne = figura.ruchy_pseudo_legalne(self.plansza_wlasna)
            for ruch in pseudo_legalne:
                if self.sprawdz_czy_legalny(ruch):
                    return True
        return False
        
        

    def get_plansza(self):
        return self.plansza_wlasna
    
    def get_figury_na_planszy(self):
        return self.gracz_bialy.get_figury_na_planszy() + self.gracz_czarny.get_figury_na_planszy()
    
    def czy_cos_sie_rusza(self):
        if self.gracz_bialy.czy_cos_sie_rusza() or self.gracz_czarny.czy_cos_sie_rusza():
            return True
        return False
    
    def porusz(self, dt):
        if self.gracz_bialy.czy_cos_sie_rusza():
            self.gracz_bialy.porusz_poruszajace(dt)
        if self.gracz_czarny.czy_cos_sie_rusza():
            self.gracz_czarny.porusz_poruszajace(dt)

    def get_poruszajace_figury(self):
        return self.gracz_bialy.get_poruszajace() + self.gracz_czarny.get_poruszajace()
    def get_zbite(self):
        return self.gracz_bialy.get_zbite() + self.gracz_czarny.get_zbite()
    
    def get_svg_planszy(self,pola_do_podswietlenia):
        fill_dict = {}
        if pola_do_podswietlenia:
            for pole in pola_do_podswietlenia:
                pozycja,r,g,b = pole
                wiersz = pozycja // 10
                kolumna = pozycja % 10
                square= chess.square(kolumna, wiersz)
                r_int = int(max(0.0, min(1.0, r)) * 255)
                g_int = int(max(0.0, min(1.0, g)) * 255)
                b_int = int(max(0.0, min(1.0, b)) * 255)
                hex_color = f"#{r_int:02x}{g_int:02x}{b_int:02x}80"
                fill_dict[square] = hex_color

        svg = chess.svg.board(
            self.plansza,
            orientation=self.tura,
            borders=True,
            fill=fill_dict
        )
        svg_bytes = cairosvg.svg2png(bytestring=svg.encode('utf-8'), scale=2.0)
        svg_plik = io.BytesIO(svg_bytes)
        return svg_plik
    
    def czy_promocja(self):
        gracz = self.gracz_bialy if self.tura else self.gracz_czarny
        promocja, self.pionek_do_promocji = gracz.czy_pionek_promocja()
        return promocja
    
    def wykonaj_promocje(self,na_co):
        gracz = self.gracz_bialy if self.tura else self.gracz_czarny
        ruch = gracz.wykonaj_promocje(self.pionek_do_promocji,na_co)
        self.pionek_do_promocji = None
        


        

        

        

class Gracz():
    def __init__(self, kolor):
        self.kolor = kolor
        self.czas = 300
        self.piony = [pionek(self.kolor,i) for i in range(0,8)]
        #self.piony = []
        self.krol = krol(self.kolor)
        self.hetman = [hetman(self.kolor)]
        wiersz = 0 if kolor else 70
        self.wieze = [wieza(self.kolor,wiersz), wieza(self.kolor,wiersz + 7)]
        self.skoczki = [skoczek(self.kolor,wiersz + 1), skoczek(self.kolor,wiersz + 6)]
        self.gonce = [goniec(self.kolor,wiersz + 2), goniec(self.kolor,wiersz + 5)]
        self.zbite_figury = []
        self.figury_na_planszy = self.piony + [self.krol] + self.hetman + self.wieze + self.skoczki + self.gonce
        self.czy_w_szachu = False
        self.ile_zbitych = 0
        #self.czy_w_ruchu = False
        self.figury_w_ruchu = []
        self.figura_zbijana = None

    def get_poruszajace(self):
        return self.figury_w_ruchu + [self.figura_zbijana]
    
    def get_zbite(self):
        figury = []
        if self.zbite_figury:
            for figura in self.zbite_figury:
                if not figura.czy_rusza:
                    figury.append(figura)
        return figury
    
    def get_figury_na_planszy(self):
        figury = []
        for figura in self.figury_na_planszy:
            if not figura.czy_rusza:
                figury.append(figura)
        return figury
    
    def czy_szach(self):
        return self.czy_w_szachu
    def ustaw_szach(self,szach):
        self.czy_w_szachu = szach
    def pozycja_krola(self):
        return self.krol.get_pozycja()
    
    def rozpocznij_ruch(self,plansza,ruch):
        self.figury_w_ruchu.append(plansza[ruch[0]%10][ruch[0]//10])
        if ruch[2] == "podwojny":
            plansza[ruch[0]%10][ruch[0]//10].czy_do_przelotu = True

        plansza[ruch[0]%10][ruch[0]//10].rozpocznij_ruch(ruch[1])
        
        if ruch[2] == "roszada_krotka":
            self.figury_w_ruchu.append(self.wieze[1])
            self.wieze[1].rozpocznij_ruch(ruch[1]-1)
        elif ruch[2] == "roszada_dluga":
            self.figury_w_ruchu.append(self.wieze[0])
            self.wieze[0].rozpocznij_ruch(ruch[1]+1)
        
        # zabranianie roszad
        if self.figury_w_ruchu[0] == self.krol:
            self.krol.zeruj_obie_roszady()
        elif self.figury_w_ruchu[0] == self.wieze[0]:
            self.krol.czy_roszada_dluga = False
        elif self.figury_w_ruchu[0] == self.wieze[1]:
            self.krol.czy_roszada_krotka = False
        
        
    def porusz_poruszajace(self,dt):
        if len(self.figury_w_ruchu) != 0:
            for i,figura in enumerate(self.figury_w_ruchu):
                czy_skonczyla = figura.przesun(dt)
                if czy_skonczyla:
                    self.figury_w_ruchu.pop(i)
        if self.figura_zbijana is not None:
            czy_skonczyla = self.figura_zbijana.przesun(dt)
            if czy_skonczyla:
                self.figura_zbijana = None

        
    
    def czy_cos_sie_rusza(self):
        if len(self.figury_w_ruchu) == 0 and self.figura_zbijana == None:
            return False
        else:
            return True

    def rozpocznij_zbicie(self, plansza, ruch):
        if ruch[2] == "bicie":
            self.figura_zbijana = plansza[ruch[1]%10][ruch[1]//10]
        elif ruch[2] == "przelot":
            self.figura_zbijana = plansza[ruch[1]%10][ruch[0]//10]
        else:
            return

        self.zbite_figury.append(self.figura_zbijana)
        self.figura_zbijana.pozycja_zbitego = self.ile_zbitych
        self.ile_zbitych += 1

        for i, figura in enumerate(self.figury_na_planszy):
            if figura == self.figura_zbijana:
                self.figury_na_planszy.pop(i)

        # Oblicz docelowy xyz 
        idx = self.figura_zbijana.pozycja_zbitego
        kolumna = idx % 2
        wiersz = idx // 2

        if self.figura_zbijana.kolor == False:  # czarna figura zbita 
            x_offset = 11 + (kolumna * 1.5)
            y_offset = -7 + (wiersz * 2)
        else:  # biała figura zbita 
            x_offset = -12 - (-kolumna * 1.5)
            y_offset = 7 + (-wiersz * 2)

        docelowy_xyz = [x_offset, y_offset, 0]
        self.figura_zbijana.rozpocznij_zbijanie(docelowy_xyz)

    def resetuj_przelot(self):
        for pionek in self.piony:
            pionek.czy_do_przelotu = False

    def czy_pionek_promocja(self):
        wiersz = 7 if self.kolor else 0
        for pionek in self.piony:
            if pionek.get_pozycja()//10 == wiersz:
                return True, pionek
        return False, None
    
    def wykonaj_promocje(self,pionek,na_co):
        match na_co:
            case 0:
                nowa_figura = hetman(self.kolor,pionek.get_pozycja())
                figura_chess = chess.QUEEN
            case 1:
                nowa_figura = wieza(self.kolor,pionek.get_pozycja())
                figura_chess = chess.ROOK
            case 2:
                nowa_figura = goniec(self.kolor,pionek.get_pozycja())
                figura_chess = chess.BISHOP
            case 3:
                nowa_figura = skoczek(self.kolor,pionek.get_pozycja())
                figura_chess = chess.KNIGHT
        self.figury_na_planszy.append(nowa_figura)
        
            