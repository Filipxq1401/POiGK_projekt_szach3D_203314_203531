from czesc_3d.model_3d import model_3d
import numpy as np
PREDKOSC = 4
class figura:
    model_bialy = None
    model_czarny = None
    plik_bialy = ""
    plik_czarny = ""
    tex_id_bialy = None
    tex_id_czarny = None

    def __init__(self, kolor, pozycja_poczatkowa):
        klasa = self.__class__
        self.kolor = kolor
        self.pozycja = pozycja_poczatkowa
        self.xyz_poczatkowe = []
        self.xyz_aktualne = []
        self.xyz_docelowe = []
        self.kierunek_ruchu = []
        self.czy_rusza = False
        self.pozycja_zbitego = None
        self.kierunki = []
        
        #--------------- wczytanie modelu i tekstury ---------------------
        if kolor:
            if klasa.model_bialy is None:
                if figura.tex_id_bialy is None:
                    klasa.model_bialy = model_3d(klasa.plik_bialy, tekstura="White_Base_color.png", centruj=True)
                    figura.tex_id_bialy = klasa.model_bialy.tex_id
                else:
                    klasa.model_bialy = model_3d(klasa.plik_bialy, tekstura_id=figura.tex_id_bialy, centruj=True)   
        else:
            if klasa.model_czarny is None:
                if figura.tex_id_czarny is None:
                    klasa.model_czarny = model_3d(klasa.plik_czarny, tekstura="Black_Base_color.png", centruj=True)
                    figura.tex_id_czarny = klasa.model_czarny.tex_id
                else:
                    klasa.model_czarny = model_3d(klasa.plik_czarny, tekstura_id=figura.tex_id_czarny, centruj=True)

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
    
    def get_xyz_na_planszy(self,offset_y = 0,offset_z = 0):
        wiersz = self.pozycja // 10
        kolumna = self.pozycja % 10
        if offset_y == 0:
            dy = 0.8 if self.kolor else 0.2
        else:
            dy = offset_y
        return [-7 + 2 * kolumna ,  -7 + 2 * wiersz + dy, 2 + offset_z]



    def __str__(self):
        klasa = self.__class__.__name__
        skrot = klasa[0].upper() if klasa != "skoczek" else "N" #
        return skrot if self.kolor else skrot.lower()
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
    
    def rozpocznij_ruch(self,docelowe):
        self.czy_rusza = True
        klasa = self.__class__
        self.xyz_aktualne = np.array(klasa.get_xyz_na_planszy(self))
        self.pozycja = docelowe
        self.xyz_docelowe = np.array(klasa.get_xyz_na_planszy(self))

    def rozpocznij_zbijanie(self):
        self.czy_rusza = True
        klasa = self.__class__
        self.xyz_aktualne = np.array(klasa.get_xyz_na_planszy(self))
        self.xyz_docelowe = np.array([20, 20, 20])

    def przesun(self,dt):
        try:
            roznica = self.xyz_docelowe - self.xyz_aktualne
            roznica_dlugosc = np.linalg.norm(roznica)
            kierunek = roznica / roznica_dlugosc # wektor jednostkowy
            przesuniecie = kierunek * PREDKOSC * dt
            if roznica_dlugosc < np.linalg.norm(przesuniecie):
                self.czy_rusza = False
                return True
            self.xyz_aktualne += kierunek * PREDKOSC * dt
            return False
        except:
            self.czy_rusza = False
            return True





    
class pionek(figura):
    plik_bialy = "White_pawn.obj"
    plik_czarny = "Black_pawn.obj"
    def __init__(self, kolor, kolumna):
        if kolor:
            pozycja = 10 + kolumna
        else:
            pozycja = 60 + kolumna
        super().__init__(kolor,pozycja)
        
        self.czy_do_przelotu = False #w jakiej turze ruszył się o 2, do bicia w przelocie

    def get_xyz_na_planszy(self):
        return  super().get_xyz_na_planszy(0.5,0)
    
    
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
            if plansza[kolumna_sprawdzana][wiersz] is not None and isinstance(plansza[kolumna_sprawdzana][wiersz],pionek) and plansza[kolumna_sprawdzana][wiersz].czy_do_przelotu and plansza[kolumna_sprawdzana][wiersz].get_kolor() != self.kolor:
                ruchy.append([wiersz*10+kolumna, (wiersz + strona_ruchu)*10+kolumna_sprawdzana, "przelot"])

        return ruchy

class krol(figura):
    plik_bialy = "White_king.obj"
    plik_czarny = "Black_king.obj"
    def __init__(self, kolor):
        if kolor:
            pozycja = 4
        else:
            pozycja = 74
        super().__init__(kolor, pozycja)

        self.czy_roszada_dluga = True # czy może zrobić roszadę
        self.czy_roszada_krotka = True

    def get_xyz_na_planszy(self):
        return  super().get_xyz_na_planszy(0,0.5)
    
    def zeruj_obie_roszady(self):
        self.czy_roszada_dluga = False # czy może zrobić roszadę
        self.czy_roszada_krotka = False
    
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
        if self.czy_roszada_krotka:
            if plansza[kolumna+1][wiersz] is None and plansza[kolumna+2][wiersz] is None and isinstance(plansza[kolumna+3][wiersz],wieza) and plansza[kolumna+3][wiersz].get_kolor() == self.kolor:
                ruchy.append([wiersz*10+kolumna, wiersz*10+kolumna+2, "roszada_krotka"])
        if self.czy_roszada_dluga:
            if plansza[kolumna-1][wiersz] is None and plansza[kolumna-2][wiersz] is None and plansza[kolumna-3][wiersz] is None and isinstance(plansza[kolumna-4][wiersz],wieza) and plansza[kolumna-4][wiersz].get_kolor() == self.kolor:
                ruchy.append([wiersz*10+kolumna, wiersz*10+kolumna-2, "roszada_dluga"])
        return ruchy
    
class hetman(figura):
    plik_bialy = "White_queen.obj"
    plik_czarny = "Black_queen.obj"
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

    def get_xyz_na_planszy(self):
        return  super().get_xyz_na_planszy(0,0.5)

class skoczek(figura):
    plik_bialy = "White_knight.obj"
    plik_czarny = "Black_knight.obj"
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
    plik_bialy = "White_rook.obj"
    plik_czarny = "Black_rook.obj"
    def __init__(self, kolor, pozycja_poczatkowa):
        super().__init__(kolor, pozycja_poczatkowa)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                if i == 0 or j == 0:
                    self.kierunki.append((i,j))

class goniec(figura):
    plik_bialy = "White_bishop.obj"
    plik_czarny = "Black_bishop.obj"
    def __init__(self, kolor, pozycja_poczatkowa):
        super().__init__(kolor, pozycja_poczatkowa)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                if not(i == 0 or j == 0):
                    self.kierunki.append((i,j))

    def get_xyz_na_planszy(self):
        return  super().get_xyz_na_planszy(0,0.5)

        
