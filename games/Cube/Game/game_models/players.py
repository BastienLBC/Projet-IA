
import random
from tkinter import *

class Player:

    def __init__(self,name:str, color:str)-> None:
        self.name = name
        self.color = color
        self.wins = 0
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

class AiPlayer(Player):
    """
    classe qui représente une IA
    """
    def __init__(self, name: str, color:str,learning_rate : float=0.01, gamma:float = 0.9, epsilon: float = 0.9) -> None:
        super().__init__(name,color)
        self.lr = learning_rate #tx d'apprentissage
        self.gamma = gamma #actualisation
        self.eps = epsilon #exploration
        self.q_table = {}

    def reward(self):
       
        ennemy = self.game.players1 if self == self.game.players2 else self.game.players2
        point_ennemy = 1
        
        if ennemy.point > point_ennemy:
            point_ennemy == ennemy.point
            self.reward -= 1
            ennemy.reward += 1
        return self.reward, ennemy.reward

    def exploit(self):
        best_move = None
        best_value = float('-inf')

        x, y = self.x, self.y
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board and 0 <= ny < self.board:  
                reward = self.q_table.get((nx, ny), 0)  
                if reward > best_value:
                    best_value = reward
                    best_move = (nx, ny)
        return best_move
