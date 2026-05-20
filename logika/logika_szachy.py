import chess

class Logika_szachy():
    def __init__(self):
        self.plansza = chess.Board()

    def wykonaj_ruch(self,ruch):
        if self.plansza.is_legal(ruch):
            self.plansza.push_san(ruch)
            return True
        else:
            return False
        
    def cofnij_ruch(self):
        self.plansza.pop()
        