
class kart:
    
    def __init__(self,name:str, x:int, y:int, speed:int):

        self.name = name
        self.x = x
        self.y = y 
        self.direction = "Est"
        self.speed = 0
        self.laps = 0
        self.inLife = True

        self.wins = 0
        self.losses = 0


    def play(self):
        """
        Retourne une direction reçu par l'utilisateur
        """
        #commence en direction EST
        return self.event
    
    def win(self) -> None:
        """
        Ajoute une victoire au nb de victoires
        """
        self.wins += 1

    def lose(self) -> None:
        """
        Ajoute une défaite au nb de défaites
        """
        self.losses += 1