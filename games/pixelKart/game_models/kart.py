import random

class kart:
    
    def __init__(self,name:str, x:int, y:int):

        self.name = name
        self.x = x
        self.y = y 
        self.direction = "Est"
        self.speed = 0
        self.laps = 0
        self.inLife = True

        self.wins = 0
        self.losses = 0

    @staticmethod
    def play(self):
        """
        Retourne une direction reçu par l'utilisateur
        """
        #commence en direction EST
        return random.choice(['Accelerate', 'Decelerate', 'Left', 'Right', 'Nothing'])
    
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

class humanKart:
    def __init__(self, name:str, x:int, y:int):
        super().__init__(name, x, y)
        
    def play(self):
        """
        Retourne un bind reçu par l'utilisateur
        """
        return self.Event

        
        
