import chess
from logika.figury import *
import copy

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
    
    def przetworz_myszke(self,wybrane,hover):
        pola_do_podświetlenia = []
        if self.gracz_bialy.czy_szach():
            pola_do_podświetlenia.append([self.gracz_bialy.pozycja_krola(),0,0,1])
        if self.gracz_czarny.czy_szach():
            pola_do_podświetlenia.append([self.gracz_czarny.pozycja_krola(),0,0,1])
        if hover is not None:
            pola_do_podświetlenia.append([hover, 1,0,0]) # czerwone
        if wybrane is not None:
            kolumna = wybrane % 10
            wiersz = wybrane // 10
            if self.plansza_wlasna[kolumna][wiersz] and self.plansza_wlasna[kolumna][wiersz].get_kolor() == self.tura: # wybrana została dobra figura
                self.wybierz_figure(self.plansza_wlasna[kolumna][wiersz])
            else:
                if self.legalne_ruchy_wybranej_figury:
                    for ruch in self.legalne_ruchy_wybranej_figury:
                        if ruch[1] == wybrane:
                            self.wykonaj_ruch_wlasny(ruch) # kliknęte było pole na które jest możliwość ruchu
                            return pola_do_podświetlenia
                self.wybierz_figure(None)
        if self.wybrana_figura:
            if self.legalne_ruchy_wybranej_figury:
                for ruch in self.legalne_ruchy_wybranej_figury:
                    pola_do_podświetlenia.append([ruch[1],0,1,0])
        return pola_do_podświetlenia
        
    def wybierz_figure(self,figura):
        if figura is None:
            self.wybrana_figura = None
            self.legalne_ruchy_wybranej_figury = None
            return
        self.wybrana_figura = figura
        pseudo_legalne = figura.ruchy_pseudo_legalne(self.plansza_wlasna)
        self.legalne_ruchy_wybranej_figury = []
        if pseudo_legalne:
            for ruch in pseudo_legalne:
                if self.sprawdz_czy_legalny(ruch):
                    self.legalne_ruchy_wybranej_figury.append(ruch)

    
    def sprawdz_czy_legalny(self, ruch):
        plansza_po_ruchu = copy.deepcopy(self.plansza_wlasna)
        plansza_po_ruchu[ruch[1]%10][ruch[1]//10] = plansza_po_ruchu[ruch[0]%10][ruch[0]//10]
        plansza_po_ruchu[ruch[0]%10][ruch[0]//10] = None
        
        if self.tura:
            pozycja_krola = self.gracz_bialy.pozycja_krola()
            figury = self.gracz_czarny.get_figury_na_planszy()
        else:
            pozycja_krola = self.gracz_czarny.pozycja_krola()
            figury = self.gracz_bialy.get_figury_na_planszy()
        
        if pozycja_krola == ruch[0]: # jeżeli król się porusza
            pozycja_krola = ruch[1]

        for figura in figury:
            if figura.get_pozycja() != ruch[1]: # jeżeli ta figura nie ma być zbita tym ruchem
                ruchy_przeciwnika = figura.ruchy_pseudo_legalne(plansza_po_ruchu)
                if ruchy_przeciwnika:
                    for ruch_przeciwnika in ruchy_przeciwnika:
                        if ruch_przeciwnika[1] == pozycja_krola:
                            return False
        return True

    def wykonaj_ruch_wlasny(self,ruch):
        w_akt = ruch[0] // 10
        k_akt = ruch[0] % 10
        w_doc = ruch[1] // 10
        k_doc = ruch[1] % 10
        ruch_chess = chess.Move(chess.square(k_akt,w_akt),chess.square(k_doc,w_doc))
        self.plansza_wlasna[k_akt][w_akt].porusz(ruch[1])
        if ruch[2] == "bicie":
            self.plansza_wlasna[k_doc][w_doc].zbij()
        self.wykonaj_ruch(self.plansza.san(ruch_chess))
        self.wybierz_figure(None)
        self.stworz_nowa_plansze()
        self.tura = not self.tura
        self.numer_tury += 1
        

    def get_plansza(self):
        return self.plansza_wlasna
    def get_figury_na_planszy(self):
        return self.gracz_bialy.get_figury_na_planszy() + self.gracz_czarny.get_figury_na_planszy()

        

        

        

class Gracz():
    def __init__(self, kolor):
        self.kolor = kolor
        self.piony = [pionek(self.kolor,i) for i in range(0,8)]
        self.krol = krol(self.kolor)
        self.hetman = hetman(self.kolor)
        wiersz = 0 if kolor else 70
        self.wieze = [wieza(self.kolor,wiersz), wieza(self.kolor,wiersz + 7)]
        self.skoczki = [skoczek(self.kolor,wiersz + 1), skoczek(self.kolor,wiersz + 6)]
        self.gonce = [goniec(self.kolor,wiersz + 2), goniec(self.kolor,wiersz + 5)]
        self.zbite_figury = None
        self.figury_na_planszy = self.piony + [self.krol, self.hetman] + self.wieze + self.skoczki + self.gonce
        self.czy_w_szachu = False

    def get_figury_na_planszy(self):
        return self.figury_na_planszy
    def czy_szach(self):
        return self.czy_w_szachu
    def pozycja_krola(self):
        return self.krol.get_pozycja()