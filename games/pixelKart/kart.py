
class kart:
    
    def __init__(self,name:str, position:tuple[int,int], speed:int):

        self.name = name
        self.position = position 
        self.direction = "Est"
        self.speed = speed 

        self.wins = 0
        self.losses = 0


    def play(self):
        """
        Retourne une direction reçu par l'utilisateur
        """
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