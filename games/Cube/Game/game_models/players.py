
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

    def get_state(self):
        """
        retourne l'état (des deux joueurs) et du plataeu
        à utiliser dans le dict pour la bsd
        """
        ennemy = self.game.players1 if self == self.game.players2 else self.game.players2
        return (self.x, self.y, ennemy.x, ennemy.y, self.game.matrix, self.game.board)

    def reward(self, old_state:tuple, new_state:tuple):
        """
        calcule la récompense en fonction de si il prend une case, enclo ou si il bloque l'adversaire
        Returns:
            int: reaward
        """
        reward = 0
        ennemy = self.game.players1 if self == self.game.players2 else self.game.players2

        if self.game.matrix[new_state[0]][new_state[1]]["color"] == "white":
            reward += 1

    def creates_enclosure(self, x: int, y: int) -> bool:
        """
        verifie si le déplacement crée un enclo
        Returns:
            bool: True si le mouvement crée un enclos
        """
        reachable = [[False for _ in range(self.board)] for _ in range(self.board)]
        queue = [(x, y)]

        while queue:
            cx, cy = queue.pop(0)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < self.board and 0 <= ny < self.board and
                        not reachable[nx][ny] and
                        self.matrix[nx][ny]["color"] == "white"):
                    reachable[nx][ny] = True
                    queue.append((nx, ny))

        return any(self.matrix[i][j]["color"] == "white" and not reachable[i][j]
                   for i in range(self.board)
                   for j in range(self.board))
