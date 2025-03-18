
import random
from tkinter import *

class Player:

    def __init__(self,name:str, color:str)-> None:
        self.name = name
        self.color = color

        self.x = 0
        self.y = 0

        self.score = 1

    @staticmethod
    def play():
        """
        Retourne un bind random
        """
        return random.choice(['Z', 'S', 'Q', 'D'])
        
class HumanPlayer(Player):
    def __init__(self, name:str, color:str)-> None:
        super().__init__(name, color)

    def play(self):
        """
        Retourne un bind reçu par l'utilisateur
        """
        return self.Event
        