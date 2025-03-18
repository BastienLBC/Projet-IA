
import random
from tkinter import event

class Player:

    def __init__(self,name:str, color:str)-> None:
        self.name = name
        self.color = color

        self.x = None
        self.y = None

        self.score = 1

        @staticmethod
        def play() -> event:
            """
            Retourne un bind random
            """
            return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        
class HumanPlayer(Player):
    def __init__(self, name:str, color:str)-> None:
        super().__init__(name, color)

    def play(self)->event:
        """
        Retourne un bind reçu par l'utilisateur
        """
        return self.Event
        