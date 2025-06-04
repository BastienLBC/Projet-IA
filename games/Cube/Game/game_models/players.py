
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
                key = generate_key(
                    self.x,
                    self.y,
                    self.enemy.x,
                    self.enemy.y,
                    self.board.get_matrix_state(),
                    self.board.get_board_state(),
                    (dx, dy),
                )
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
        current_key = generate_key(*state, action)

        # Calcul du meilleur Q pour l'état suivant sur toutes les actions
        possible_actions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        next_q_values = [
            self.get_q_value(
                generate_key(
                    next_state[0],
                    next_state[1],
                    next_state[2],
                    next_state[3],
                    next_state[4],
                    next_state[5],
                    a,
                )
            )
            for a in possible_actions
        ]
        next_q = max(next_q_values)

        # Obtient les valeurs Q actuelles
        current_q = self.get_q_value(current_key)

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
        """Choisit une action et la renvoie sous forme de direction."""

        # Mémorise l'état avant déplacement pour la mise à jour après le coup
        self._old_state = (
            self.x,
            self.y,
            self.enemy.x,
            self.enemy.y,
            self.board.get_matrix_state(),
            self.board.get_board_state(),
        )

        # Choix de l'action
        self._last_action = self.choose_action()
        direction = self.action_to_direction(self._last_action)

        return direction

    def after_move(self):
        """Mise à jour de la Q-table une fois le déplacement effectué."""

        dx, dy = self._last_action
        new_x, new_y = self.x, self.y

        reward = self.calculate_reward(
            self._old_state[0],
            self._old_state[1],
            new_x,
            new_y,
        )

        new_state = (
            new_x,
            new_y,
            self.enemy.x,
            self.enemy.y,
            self.board.get_matrix_state(),
            self.board.get_board_state(),
        )

        self.update_q_table(self._old_state, self._last_action, reward, new_state)
        direction = self.action_to_direction(self._last_action)
        print(f"Reward: {reward}, Action: {direction}")

    def calculate_reward(self, from_x, from_y, to_x, to_y):
        """
        Calcule la récompense pour un déplacement
        @param from_x: Position x de départ
        @param from_y: Position y de départ
        @param to_x: Position x d'arrivée
        @param to_y: Position y d'arrivée
        @return: La récompense calculée
        """
        print(f"Reward calculated: 25 (from {from_x},{from_y} to {to_x},{to_y})")
        reward = 25  # Récompense de base pour un mouvement valide

        # Vérifier si le mouvement est valide
        if not (0 <= to_x < self.board.size and 0 <= to_y < self.board.size):
            return -50  # Pénalité pour un mouvement invalide

        # Vérifier si la case est occupée par l'adversaire
        if self.board.matrix[to_x][to_y]["color"] == self.enemy.color:
            return -50

        # Pénalité si on s'éloigne du centre
        distance_to_center = abs(to_x - self.board.size // 2) + abs(to_y - self.board.size // 2)
        reward -= distance_to_center * 2

        # Bonus si on s'approche de l'adversaire
        distance_to_enemy = abs(to_x - self.enemy.x) + abs(to_y - self.enemy.y)
        if distance_to_enemy < abs(from_x - self.enemy.x) + abs(from_y - self.enemy.y):
            reward += 10

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

        # Vérifie si le mouvement est valide
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
