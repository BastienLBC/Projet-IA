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
    def __init__(self,name: str, epsilon = 0.9, learning_rate = 0.01, historique =None, previous_state = None):
        super().__init__(name)
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
        best_value = float("inf")
        nb_torchs = self.game.nb

        for i in [1,2, 3]:
            next_state = nb_torchs - i
            next_value = self.v_function.get(next_state, 0)

            if best_move is None or next_value < best_value or (next_value == best_value and i < best_move):
                best_value = next_value
                best_move = i

        return best_move

    def play(self)->int:
        """
        Ajoute la transition des coups à l'historique,
        en fonction de l'epsilon, joue soit un nb aleatoire,
        soit le coup réfléchi par l'exploitation.
        met à jour l'état précédent
        
        Returns:
            -Int : le coup à jouer choisi par l'ia
        """
        if self.previous_state:
            self.historique.append((self.previous_state, GameModel.nb))

        #eps = proba qui choisi si on exploite ou si on explore (random)
        if random.uniform(0,1.0) < self.eps:
            move = random.randint(1,3)
        else:
            move = self.exploit()

        self.previous_state = GameModel.nb - move
        return move

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

    def train(self) -> None:
        """
        Entraîne l'IA en se basant sur l'historique.
        Parcourt l'historique à l'envers et le vide une fois terminé.
        """
        while self.historique:
            state, next_state = self.historique.pop()
            if next_state not in self.v_function:
                self.v_function[next_state] = 0  # Initialisation des états inconnus
            if state not in self.v_function:
                self.v_function[state] = 0  # Initialisation des états inconnus
            self.v_function[state] += self.lr * (self.v_function[next_state] - self.v_function[state])

    def next_epsilon(self, coef: float = 0.95, min: float = 0.05) -> None:
        """
        Fait varier l'epsilon mais il ne descend jamais en dessous de 0.05
        """
        self.eps = max(self.eps * coef, min)
