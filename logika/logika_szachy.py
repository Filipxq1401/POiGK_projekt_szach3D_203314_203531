import chess

class Logika_szachy():
    def __init__(self):
        self.plansza = chess.Board()

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
        self.plansza.pop()
        