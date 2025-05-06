
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
        self.board = None
        self.q_table = {}

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

    def update_q_table(self, state, action, reward, next_state):
        """
        Met à jour la table Q avec la nouvelle valeur calculée
        """
        # Génère les clés pour l'état actuel et suivant
        current_key = generate_key(*state)
        next_key = generate_key(*next_state)

        # Obtient les valeurs Q actuelles
        current_q = self.get_q_value(current_key)
        next_q = self.get_q_value(next_key)

        # Calcule la nouvelle valeur Q
        new_q = current_q + self.lr * (reward + self.gamma * next_q - current_q)

        # Sauvegarde la nouvelle valeur
        self.set_q_value(current_key, new_q)
        print(f"Updated Q-value for {current_key}: {new_q}")

    def action_to_direction(self, action):
        """
        Convertit une action (dx, dy) en direction (UP, DOWN, LEFT, RIGHT)
        """
        dx, dy = action
        if dx == 0 and dy == -1:
            return 'UP'
        elif dx == 0 and dy == 1:
            return 'DOWN'
        elif dx == -1 and dy == 0:
            return 'LEFT'
        elif dx == 1 and dy == 0:
            return 'RIGHT'
        return None

    def play(self):
        old_x, old_y = self.x, self.y
        old_state = (self.x, self.y, self.enemy.x, self.enemy.y,
                     self.board.get_matrix_state(), self.board.get_board_state())

        action = self.choose_action()
        direction = self.action_to_direction(action)

        # Calcule la nouvelle position sans l'appliquer
        dx, dy = action
        new_x, new_y = self.x + dx, self.y + dy

        # Calcule la récompense
        reward = self.calculate_reward(old_x, old_y, new_x, new_y)

        # Calcule le nouvel état sans l'appliquer
        new_state = (new_x, new_y, self.enemy.x, self.enemy.y,
                     self.board.get_matrix_state(), self.board.get_board_state())

        # Met à jour la table Q
        self.update_q_table(old_state, action, reward, new_state)
        print(f"Reward: {reward}, Action: {direction}")

        return direction

    def calculate_reward(self, previous_state, current_state):
        """
        Calcule la récompense basée sur la transition entre l'état précédent et l'état actuel.

        Args:
            previous_state (dict): L'état du plateau avant l'action.
            current_state (dict): L'état du plateau après l'action.

        Returns:
            float: La récompense calculée.
        """
        reward = 0

        # Récompense pour les cases capturées
        previous_score = previous_state["current_player"]["score"]
        current_score = current_state["current_player"]["score"]
        reward += (current_score - previous_score) * 10  # Exemple : 10 points par case capturée

        # Pénalité si le joueur perd une case
        previous_opponent_score = previous_state["opponent"]["score"]
        current_opponent_score = current_state["opponent"]["score"]
        reward -= (current_opponent_score - previous_opponent_score) * 5  # Exemple : -5 points par case perdue

        # Récompense pour avoir enfermé des cases
        if "enclosed_areas" in current_state:
            reward += len(current_state["enclosed_areas"]) * 15  # Exemple : 15 points par zone enfermée

        # Autres règles spécifiques
        if current_state["game_over"]:
            if current_state["winner"] == "current_player":
                reward += 100  # Bonus pour gagner
            else:
                reward -= 100  # Pénalité pour perdre

        return reward

    def is_valid_move(self, x, y):
        """Vérifie si un mouvement est valide"""
        if x < 0 or y < 0 or x >= len(self.board) or y >= len(self.board):
            return False
        if self.board[x][y] == (3 - self.player_turn):  # Case appartient à l'adversaire
            return False
        return True

    def count_player_cells(self, player, board_after=None):
        """Compte le nombre de cases possédées par un joueur"""
        board = board_after if board_after else self.board
        return sum(row.count(player) for row in board)

    def move(self, dx, dy):
        """
        Met à jour la position du joueur en fonction des décalages dx et dy.
        """
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < self.board.size and 0 <= new_y < self.board.size:
            self.x = new_x
            self.y = new_y

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