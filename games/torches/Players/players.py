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

class ai_player(Player):
    """
    Classe qui représente un player AI (qui hérite de player)
    redéfini play 
    """
    def __init__(self, name: str, game=None, epsilon: float = 0.9, learning_rate: float = 0.01, historique: list[int] = None, previous_state: int = None) -> None:
        super().__init__(name, game)
        self.eps = epsilon
        self.lr = learning_rate
        self.historique = historique if historique is not None else []
        #self.historique = [] or historique
        self.previous_state = previous_state
        self.v_function = {
            "lose":-1,
            "win":1,
        }
        for i in range(13):
            self.v_function[i] = 0

    def exploit(self)->int:
        """
        trouve la meilleure action à jouer en calculant pour chaque action,
        l'état d'après le coup (pour avoir l'état où se trouvera l'adversaire)

        Returns:
            int: la meilleure action entre 1 et 3,
            où la plus petite action est le moins bon pour l'adversaire
        """
        possible_actions = {}

        for action in range(1,4):
            next_state = self.game.nb - action
            state_value = self.v_function.get(next_state, 0)
            possible_actions[action] = state_value

        return min(possible_actions, key=possible_actions.get) 

    def play(self)->int:
        """
        Ajoute la transition des coups à l'historique,
        en fonction de l'epsilon, joue soit un nb aleatoire,
        soit le coup réfléchi par l'exploitation.
        met à jour l'état précédent
        (exploit doit être 1, 2 ou 3)
        
        Returns:
            -Int : le coup à jouer choisi par l'ia (action)
        """
        if self.previous_state:
            self.historique.append((self.previous_state, self.game.nb))

        #eps = proba qui choisi si on exploite (move réfléchi) ou si on explore (random move)
        if random.uniform(0,1.0) < self.eps:
            move = random.randint(1,3)
        else:
            move = self.exploit()

        self.previous_state = self.game.nb - move # met à jour l'état
        return move

    def win(self) -> None:
        """
        Ajoute une victoire à l'ia, et met à jour la transition
        """
        super().win()
        self.historique.append((self.previous_state, self.v_function["win"]))
        self.previous_state = None

    def lose(self) -> None:
        """
        Ajoute une défaite à l'ia, et met à jour la transition
        """
        super().lose()
        self.historique.append((self.previous_state, self.v_function["lose"]))
        self.previous_state = None

    def train(self)->None:
        """
        entraine l'ia avec la v function.
        en utilisant la formule V(s) = v(s) + learning rate * [v(s')- v(s)]
        et vide l'historique
        """
        for state, next_state in reversed(self.historique):
            current_value = self.v_function.get(state, 0)
            if state not in self.v_function:
                self.v_function[state] = 0

            next_value = self.v_function.get(next_state, 0) if isinstance(next_state, int) else 0
            self.v_function[state] = current_value + self.lr * (next_value - current_value)

        self.historique.clear()

    def next_epsilon(self, coef=0.95, min=0.05)->None:
        """
        réduit l'epsilon pour utiliser + l'exploitation au fur et à mesure
        
        Args:
            coef (float): coefficient de réduction
            min (float): valeur min d'epsilon
        """
        self.eps = self.eps * coef
        if self.eps < min:
            self.eps = min
    
    