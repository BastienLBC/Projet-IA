"""
Module qui gère les différents types de joueurs
"""
import random
from Game.game_model import *

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
    """
    Classe qui représente un player AI (qui hérite de player)
    redéfini play 
    """
    def __init__(self,name:str, game=None, epsilon: float = 0.9, learning_rate: float= 0.01, historique: list[int]=None, previous_state: int= None)->None:
        super().__init__(name,game)
        self.eps= epsilon
        self.lr = learning_rate
        self.historique = [] or historique
        self.previous_state = previous_state
        self.v_function = {"lose":-1, "win":1}

    def exploit():
        pass

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
    
    def win(self)->None:
        pass
