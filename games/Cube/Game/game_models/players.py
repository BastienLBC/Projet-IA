
import random
from tkinter import *
from Game.dico import generate_key
from Game.dao import find_entry_by_key, save_entry

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
    def __init__(self, name: str, color: str, learning_rate: float = 0.01, gamma: float = 0.9, epsilon: float = 0.9) -> None:
        super().__init__(name, color)
        self.lr = learning_rate
        self.gamma = gamma
        self.eps = epsilon

    def get_q_value(self, key):
        entry = find_entry_by_key(key)
        return entry['reward'] if entry else 0.0

    def set_q_value(self, key, reward):
        save_entry({'unique_key': key, 'reward': reward})

    def choose_action(self):
        import random
        actions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if random.random() < self.eps:
            return random.choice(actions)  # Exploration
        else:
            return self.exploit(actions)   # Exploitation

    def exploit(self, actions):
        best_action = None
        best_value = float('-inf')
        for dx, dy in actions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < self.board.size and 0 <= ny < self.board.size:
                key = generate_key(self.x, self.y, self.enemy.x, self.enemy.y, self.board.get_matrix_state(), self.board.get_board_state())
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

    def play_turn(self):
        # Sauvegarde l'état actuel
        old_state = (self.x, self.y, self.enemy.x, self.enemy.y,
                     self.board.get_matrix_state(), self.board.get_board_state())

        action = self.choose_action()
        dx, dy = action
        self.move(dx, dy)

        # Récompense immédiate
        reward = self.calculate_reward()

        # État après action
        new_state = (self.x, self.y, self.enemy.x, self.enemy.y,
                     self.board.get_matrix_state(), self.board.get_board_state())

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
            return 0.0

def train_ai(ai_player, opponent, game, episodes=1000, epsilon_decay=0.995, min_epsilon=0.1):
    """
    Entraîne une IA contre un adversaire sur un certain nombre de parties.

    :param ai_player: instance de AiPlayer
    :param opponent: adversaire (peut être un autre AiPlayer ou un joueur aléatoire)
    :param game: instance du jeu
    :param episodes: nombre de parties
    :param epsilon_decay: facteur de réduction de epsilon par épisode
    :param min_epsilon: epsilon minimum (exploration minimale)
    """
    for episode in range(episodes):
        game.reset()  # Remet le plateau et les positions à zéro
        current_player = game.players1  # ou une logique pour alterner entre les joueurs

        # Joue jusqu'à ce que la partie soit finie
        while not game.is_finished():
            # L'IA choisit son action et la joue
            if isinstance(current_player, AiPlayer):
                current_player.play_turn()

            # L'adversaire joue son tour (si c'est un joueur aléatoire ou un autre IA)
            else:
                current_player.play()  # L'adversaire fait un coup aléatoire

            # Après chaque tour, on change de joueur
            game.switch_player()

        # Réduction progressive de l'exploration (epsilon)
        if ai_player.eps > min_epsilon:
            ai_player.eps *= epsilon_decay

        # Affichage tous les 100 épisodes
        if (episode + 1) % 100 == 0 or episode == 0:
            print(f"Épisode {episode + 1}/{episodes} - Epsilon: {ai_player.eps:.4f}")


    @property
    def enemy(self):
        return self.game.players1 if self == self.game.players2 else self.game.players2