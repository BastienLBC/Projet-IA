
import random
from tkinter import *
from Game.dico import generate_key
from Game.dao import find_entry_by_key, save_entry

from Game.game_models.game_model import GameModel

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
    Classe qui représente une IA
    """

    def __init__(self, name: str, color: str, learning_rate: float = 0.01, gamma: float = 0.9,
                 epsilon: float = 0.9) -> None:
        super().__init__(name, color)
        self.lr = learning_rate
        self.gamma = gamma
        self.eps = epsilon

    def get_q_value(self, key):
        entry = find_entry_by_key(key)
        q_value = entry['reward'] if entry else 0.0
        print(f"Loaded Q-value for {key}: {q_value}")  # vérifie le chargement des valeurs
        return q_value

    def set_q_value(self, key, reward):
        save_entry({'unique_key': key, 'reward': reward})

    def choose_action(self):
        actions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if random.random() < self.eps:
            return random.choice(actions)  # Exploration
        else:
            return self.exploit(actions)  # Exploitation

    def exploit(self, actions):
        best_action = None
        best_value = float('-inf')
        for dx, dy in actions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < self.board.size and 0 <= ny < self.board.size:
                key = generate_key(self.x, self.y, self.enemy.x, self.enemy.y, self.board.get_matrix_state(),
                                   self.board.get_board_state())
                q_value = self.get_q_value(key)
                if q_value > best_value:
                    best_value = q_value
                    best_action = (dx, dy)
        return best_action

    def update_q_table(self, old_state, action, reward, new_state):
        """
        old_state / new_state: tuple (x, y, ennemy_x, ennemy_y, matrix_state, board_state)
        """
        old_key = generate_key(*old_state)
        new_key = generate_key(*new_state)

        old_q = self.get_q_value(old_key)
        future_q = self.get_q_value(new_key)

        updated_q = old_q + self.lr * (reward + self.gamma * future_q - old_q)
        self.set_q_value(old_key, updated_q)
        print(f"Updated Q-value for {old_key}: {updated_q}")  # vérifie mises à jour

    def play_turn(self):
        # Sauvegarde l'état actuel
        self.previous_score = self.score
        self.enemy.previous_score = self.enemy.score

        # Récupère l'état actuel
        old_state = (self.x, self.y, self.enemy.x, self.enemy.y,
                    self.board.get_matrix_state(), self.board.get_board_state())
        old_key = generate_key(*old_state)

        # Choix de l'action
        action = self.choose_action()
        dx, dy = action
        self.move(dx, dy)

        # Calcul de la récompense
        reward = self.calculate_reward()

        # Nouvel état après mouvement
        new_state = (self.x, self.y, self.enemy.x, self.enemy.y,
                 self.board.get_matrix_state(), self.board.get_board_state())
        new_key = generate_key(*new_state)

        # Logging
        print("====== TOUR DE L'IA ======")
        print(f"Ancien état clé: {old_key}")
        print(f"Nouvel état clé: {new_key}")
        print(f"Action choisie: dx={dx}, dy={dy}")
        print(f"Récompense reçue: {reward}")
        print(f"Ancien Q: {self.get_q_value(old_key)}")
        print(f"Futur Q: {self.get_q_value(new_key)}")
        print(f"Epsilon actuel: {self.eps}")
        print("==========================\n")

        # Mise à jour Q-table
        self.update_q_table(old_state, action, reward, new_state)


    def calculate_reward(self):
        """
        Simple règle de récompense (exemple): +1 si IA gagne un point, -1 si ennemi en gagne.
        """
        if self.point > self.enemy.point:
            return 1.0
        elif self.point < self.enemy.point:
            return -1.0
        else:
            return -0.01

    def next_epsilon(self, coef: float = 0.95, min: float = 0.05) -> None:
        """
        Réduit l'epsilon pour favoriser l'exploitation au fil du temps.
        L'epsilon ne descend jamais en dessous du minimum spécifié.
        """
        self.eps = self.eps * coef
        if self.eps < min:
            self.eps = min

    @property
    def enemy(self):
        return self.game.players1 if self == self.game.players2 else self.game.players2