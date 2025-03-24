
import random
from tkinter import *

class Player:

    def __init__(self,name:str, color:str)-> None:
        self.name = name
        self.color = color
        self.win = 0
        self.losses = 0
        
        self.x = 0
        self.y = 0

        self.score = 1

    @staticmethod
    def play():
        """
        Retourne un bind random
        """
        return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    
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
        
class HumanPlayer(Player):
    def __init__(self, name:str, color:str)-> None:
        super().__init__(name, color)

    def play(self):
        """
        Retourne un bind reçu par l'utilisateur
        """
        return self.Event
        