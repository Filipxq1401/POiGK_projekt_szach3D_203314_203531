from czesc_3d.model_3d import model_3d
class figura:
    model_bialy = None
    model_czarny = None
    plik_modelu = ""
    tex_id_bialy = None
    tex_id_czarny = None

    def __init__(self, kolor, pozycja_poczatkowa):
        klasa = self.__class__
        self.kolor = kolor
        self.pozycja = pozycja_poczatkowa
        self.poprzednia_pozycja = pozycja_poczatkowa
        self.czy_rusza = False
        self.pozycja_zbitego = None
        self.kierunki = []
        #--------------- wczytanie modelu i tekstury ---------------------
        if kolor:
            if klasa.model_bialy is None:
                if figura.tex_id_bialy is None:
                    klasa.model_bialy = model_3d(klasa.plik_modelu,tekstura="białe_piony.jpg")
                    figura.tex_id_bialy = klasa.model_bialy.tex_id
                else:
                    klasa.model_bialy = model_3d(klasa.plik_modelu,tekstura_id = figura.tex_id_bialy)   
        else:
            if klasa.model_czarny is None:
                if figura.tex_id_czarny is None:
                    klasa.model_czarny = model_3d(klasa.plik_modelu,tekstura="Czarne_piony.jpg")
                    figura.tex_id_czarny = klasa.model_czarny.tex_id
                else:
                    klasa.model_czarny = model_3d(klasa.plik_modelu,tekstura_id = figura.tex_id_czarny)

    def get_kolor(self):
        return self.kolor
    
    def wyswietl(self):
        klasa = self.__class__
        if(self.kolor):
            klasa.model_bialy.rysuj()
        else:
            klasa.model_czarny.rysuj()
    
    def porusz(self,nowa_pozycja):
        self.pozycja = nowa_pozycja
    def zbij(self):
        self.pozycja = 88
    def get_pozycja(self):
        return self.pozycja
    def __str__(self):
        klasa = self.__class__
        nazwa = klasa.plik_modelu
        if(self.kolor):
            nazwa = nazwa.lower()
        return nazwa
    def ruchy_pseudo_legalne(self, plansza):
        if self.pozycja == 88:
            return []
        kolumna = self.pozycja % 10
        wiersz = self.pozycja // 10

        ruchy = []
        for i,j in self.kierunki:
            przesuniecie = 0
            wolne = True
            while wolne:
                przesuniecie += 1
                kolumna_sprawdzana = kolumna + i * przesuniecie
                wiersz_sprawdzany = wiersz + j * przesuniecie
                if kolumna_sprawdzana not in range(8) or wiersz_sprawdzany not in range(8):
                    wolne = False
                elif plansza[kolumna_sprawdzana][wiersz_sprawdzany] is None:
                    ruchy.append([wiersz*10+kolumna, wiersz_sprawdzany*10+kolumna_sprawdzana, "normalny"]) # puste pole, możliwe dalsze przesunięcie w tą strone
                elif plansza[kolumna_sprawdzana][wiersz_sprawdzany].get_kolor() != self.kolor:
                    ruchy.append([wiersz*10+kolumna, wiersz_sprawdzany*10+kolumna_sprawdzana, "bicie"])  #pole zajęte przez przeciwnika, nie możliwe dalsze przesunięcie w tą strone
                    wolne = False
                else:
                    wolne = False #pole zajęte przez inna figure tego samego koloru, nie możliwe dalsze przesunięcie w tą strone
        return ruchy


    
class pionek(figura):
    plik_modelu = "Pawn.obj"
    def __init__(self, kolor, kolumna):
        if kolor:
            pozycja = 10 + kolumna
        else:
            pozycja = 60 + kolumna
        super().__init__(kolor,pozycja)
        
        self.czy_do_przelotu = False #w jakiej turze ruszył się o 2, do bicia w przelocie
    
    def get_czy_przelot(self):
        return self.czy_do_przelotu
    
    def ruchy_pseudo_legalne(self, plansza):
        if self.pozycja == 88:
            return []
        kolumna = self.pozycja % 10
        wiersz = self.pozycja // 10

        ruchy = []
        strona_ruchu = 1 if self.kolor else -1
        wiersz_do_2 = 1 if self.kolor else 6
        if wiersz == 0 or wiersz == 7:
            return ruchy
        if plansza[kolumna][wiersz + strona_ruchu] is None:
            ruchy.append([wiersz*10+kolumna, (wiersz + strona_ruchu)*10+kolumna, "normalny"])
        if wiersz == wiersz_do_2 and plansza[kolumna][wiersz + strona_ruchu] is None and plansza[kolumna][wiersz + 2*strona_ruchu] is None:
            ruchy.append([wiersz*10+kolumna, (wiersz + 2*strona_ruchu)*10+kolumna, "podwojny"])
        for strona in [-1,1]:
            kolumna_sprawdzana = kolumna + strona
            if kolumna_sprawdzana not in range(8):
                continue
            if plansza[kolumna_sprawdzana][wiersz + strona_ruchu] is not None and plansza[kolumna_sprawdzana][wiersz + strona_ruchu].get_kolor() != self.kolor:
                ruchy.append([wiersz*10+kolumna, (wiersz + strona_ruchu)*10+kolumna_sprawdzana, "bicie"])
            # jeszcze bicie w przelocie wymyśleć
        return ruchy

class krol(figura):
    plik_modelu = "King.obj"
    def __init__(self, kolor):
        if kolor:
            pozycja = 4
        else:
            pozycja = 74
        super().__init__(kolor, pozycja)

        self.czy_roszada = True # czy może zrobić roszadę
    
    def get_czy_roszada(self):
        return self.czy_roszada
    
    def ruchy_pseudo_legalne(self, plansza):
        if self.pozycja == 88:
            return []
        kolumna = self.pozycja % 10
        wiersz = self.pozycja // 10

        ruchy = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                kolumna_sprawdzana = kolumna + i
                wiersz_sprawdzany = wiersz + j
                if kolumna_sprawdzana not in range(8) or wiersz_sprawdzany not in range(8):
                    continue
                if plansza[kolumna_sprawdzana][wiersz_sprawdzany] is None:
                    ruchy.append([wiersz*10+kolumna, wiersz_sprawdzany*10+kolumna_sprawdzana, "normalny"])
                elif plansza[kolumna_sprawdzana][wiersz_sprawdzany].get_kolor() != self.kolor:
                    ruchy.append([wiersz*10+kolumna, wiersz_sprawdzany*10+kolumna_sprawdzana, "bicie"])
        # jeszcze sprawdzenie roszady
        return ruchy
    
class hetman(figura):
    plik_modelu = "Queen.obj"
    def __init__(self, kolor, pozycja_poczatkowa = None):
        if kolor:
            pozycja = 3
        else:
            pozycja = 73

        if pozycja_poczatkowa is not None:
            pozycja = pozycja_poczatkowa
        super().__init__(kolor,pozycja)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                self.kierunki.append((i,j))

class skoczek(figura):
    plik_modelu = "Knight.obj"
    def __init__(self, kolor, pozycja_poczatkowa):
        super().__init__(kolor, pozycja_poczatkowa)
        self.mozliwe_przesuniecia = []
        for i in [-2,2]:
            for j in [-1,1]:
                self.mozliwe_przesuniecia.append((i,j))
                self.mozliwe_przesuniecia.append((j,i))
    def ruchy_pseudo_legalne(self, plansza):
        if self.pozycja == 88:
            return []
        kolumna = self.pozycja % 10
        wiersz = self.pozycja // 10

        ruchy = []
        for i,j in self.mozliwe_przesuniecia:
            kolumna_sprawdzana = kolumna + i
            wiersz_sprawdzany = wiersz + j
            if kolumna_sprawdzana not in range(8) or wiersz_sprawdzany not in range(8):
                continue
            if plansza[kolumna_sprawdzana][wiersz_sprawdzany] is None:
                    ruchy.append([wiersz*10+kolumna, wiersz_sprawdzany*10+kolumna_sprawdzana, "normalny"])
            elif plansza[kolumna_sprawdzana][wiersz_sprawdzany].get_kolor() != self.kolor:
                ruchy.append([wiersz*10+kolumna, wiersz_sprawdzany*10+kolumna_sprawdzana, "bicie"])
        return ruchy
        
        

class wieza(figura):
    plik_modelu = "Rook.obj"
    def __init__(self, kolor, pozycja_poczatkowa):
        super().__init__(kolor, pozycja_poczatkowa)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                if i == 0 or j == 0:
                    self.kierunki.append((i,j))

class goniec(figura):
    plik_modelu = "Bishop.obj"
    def __init__(self, kolor, pozycja_poczatkowa):
        super().__init__(kolor, pozycja_poczatkowa)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                if not(i == 0 or j == 0):
                    self.kierunki.append((i,j))

        
