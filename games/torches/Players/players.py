"""
Module qui gère les différents types de joueurs
"""

import random
from Game.game_controller import *

# --- Player Classes ---
class Player:
    """
    Classe de base d'un joueur

    Attributes:
        name (str): nom du joueur
        game: instance du jeu
        wins (int): Nnombre de victoires
        losses (int): nombre de défaites
    """
    def __init__(self, name : str, game=None) -> None:
        """
        Initialise un nouveau joueur

        Args:
            name (str): nom du joueur
            game: Instance du jeu (facultatif)
        """
        self.name = name
        self.game = game
        self.wins = 0
        self.losses = 0

    @property
    def nb_games(self) -> int:
        """
        Calcule le nombre de parties jouées

        Returns:
            int: somme des victoires et défaites
        """
        return self.wins + self.losses

    @staticmethod
    def play() -> int:
        """
        Joue un coup aléatoire

        Returns:
            int: nombre d'allumettes à jouer de 1 à 3
        """
        return random.randint(1, 3)

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

class Human(Player):
    """
    Classe qui représente un Player humain (hérite de Player),
    et surcharge play pour que l'utilisateur rentre le nombre qu'il veut jouer
    """
    def play(self) -> int:
        return int(input(f"{self.name}, combien d'allumettes prenez-vous (1-3) ? "))
    
class ia_player(Player):
    def __init__(self, epsilon = 0.9, learning_rate = 0.01, historique =None, previous_state = None):
        super().__init__()
        self.eps= epsilon
        self.lr = learning_rate
        self.historique = [] or historique
        self.previous_state = previous_state
        self.v_function = {"lose":-1, "win":1}


def exploit(self) -> int:
    """
    choisit la pire action possible pour le donner a son adversaire
    """
    best_move = None
    best_value = 1
    nb_torchs = self.game.nb

    for i in [2, 3]:
        next_state = nb_torchs - i
        next_value = self.v_function.get(next_state, 0)

        if next_value < best_value:
            best_value = next_value
            best_move = i

    return best_move

def play(self):
    if self.previous_state is not None:
        self.historique.append((self.previous_state, self.nb_torchs))

    self.previous_state = self.nb_torchs

    return self.exploit()

def win(self) -> None:
    """
    Ajoute une victoire au nb de victoires,
    ajoute la dernière transition avec win à l'historique, 
    remets previous_state à None.
    """
    super().win()
    if self.previous_state is not None:
        self.historique.append((self.previous_state, "win"))
    self.previous_state = None

def lose(self) -> None:
    """
    Ajoute une défaite au nb de défaites,
    ajoute la dernière transition avec lose à l'historique,
    remets previous_state à None.
    """
    super().lose()
    if self.previous_state is not None:
        self.historique.append((self.previous_state, "lose"))
    self.previous_state = None
