
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
        +1 : prise case blanche
        +5 : creation d'enclo
        -0.5 : par nb de cases blanches autour de l'adversaire (pour le forcer à enfermer l'adversaire)
        +-20 : victoire/ defaite
        Returns:
            float: reaward
        """
        reward = 0
        ennemy = self.game.players1 if self == self.game.players2 else self.game.players2

        if self.game.matrix[new_state[0]][new_state[1]]["color"] == "white":
            reward += 1

        if self.is_enclosure(new_state[0], new_state[1]):
            reward += 5

        accessibles_cases = self.accessible_cases(ennemy)
        reward -= accessibles_cases * 0.5

        if self.game.is_finished():
            if self.game.get_winner() == self:
                reward += 20
            else:
                reward -= 20

        return reward

    def accessible_cases(self,player):
        """
        compte le nb de cases blanches autour d'un joueur
        Args:
            player:
        Returns:
            int : nb de cases blanches autour du player
        """
        count = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = player.x + dx, player.y + dy
            if (0 <= new_x < self.game.board and 0 <= new_y < self.game.board and
                    self.game.matrix[new_x][new_y]["color"] == "white"):
                count += 1
        return count

    def is_enclosure(self, x: int, y: int) -> bool:
        """
        verifie si le déplacement crée un enclo
        Returns:
            bool: True si le mouvement crée un encloada
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

    def play(self) -> str:
        """
        return le bind choisi par l'ia, explore ou exploite et initialise l'état si pas encore fait
        Returns:
            str : bind
        """""
        state = self.get_state()
        if state not in self.q_table:
            self.q_table[state] = {
                "UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0
            }

        if random.random() < self.eps:
            return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        else:
            return max(self.q_table[state].items(), key=lambda x: x[1])[0]
