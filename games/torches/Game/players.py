"""
Module qui gère les différents types de joueurs
"""

import random
from .game_model import *

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
    
class Ai_player(Player):
    """
    Classe qui représente un player IA, 
    il va apprendre pleins de patterns pour nous faire perdre
    """
    def __init__(self,name, game=None, eps:float=0.9, lr:float=0.01, historique:list[int]=None, previous_state:int=None):
        super().__init__(name, game)
        self.eps = eps
        self.lr = lr
        self.historique =historique or []
        self.previous_state = previous_state
        self.v_function = {"win":1, "lose":-1}
        self.previous_state = previous_state
        """
        notes pour comprendre pq win = 1 et lose -1
            Exemple avec 4 allumettes :
            V(4) = 0.2    → 20% chance de gagner
            V(3) = -0.5   → Mauvaise position  
            V(2) = 0.7    → Bonne position
            V(1) = -0.8   → Très mauvaise position
            V("win") = 1  → Victoire certaine  
            V("lose") = -1 → Défaite certaine
        """

    def exploit(self)->int:
        """
        Choisit le meilleur coup à jouer
        
        quand on rencontre un état, il sera initialisé à 0
        Utilise la v-function pour déterminer quel nombre d'allumettes
        prendre mettra l'adversaire dans la position la plus défavorable.
        au début, tout sera à 0 et il sera nul
        
        Returns:
            int: nb à jouer (1,2,3)
        """
        state = self.game.nb
        if state not in self.v_function:
            self.v_function[state] = 0

        min_value = float('inf')
        for move in range(1,4):
            next_state = state - move
            
            if next_state >= 0:
                if next_state not in self.v_function:
                    self.v_function[next_state] = 0

                if self.v_function[next_state] <= min_value:
                    best_move = move
                    min_value = self.v_function[next_state]
        
        return best_move

    def play(self)->int:
        """
        Décide si l'IA doit explorer (coup aléatoire) ou exploiter (meilleur coup).
        
        Utilise epsilon pour faire le choix:
        - Si random < epsilon: exploration (coup aléatoire)
        - Sinon: exploitation (meilleur coup via exploit())
        
        Returns:
            int: Nombre d'allumettes à prendre (1, 2 ou 3)
        """
        if self.previous_state:
            self.historique.append((self.previous_state,self.game.nb))
        
        #eps = proba qui choisi si on exploite (move réfléchi) ou si on explore (random move)
        if random.uniform(0,1) < self.eps:
            move = random.randint(1,3)
        else:
            move = self.exploit()

        self.previous_state = self.game.nb - move # met à jour l'état
        return move

    def win(self):
        """
        Ajoute une victoire au nb de victoires,
        ajoute la dernière transition avec win à l'historique, 
        remets previous_state à None.
        """
        super().win()
        if self.previous_state is not None:
            self.historique.append((self.previous_state, "win"))
        self.previous_state = None

    def lose(self):
        """
        Ajoute une défaite au nb de défaites,
        ajoute la dernière transition avec lose à l'historique,
        remets previous_state à None.
        """
        super().lose()
        if self.previous_state is not None:
            self.historique.append((self.previous_state, "lose"))
        self.previous_state = None

    def train(self):
        """
        Met à jour la value-function basée sur l'historique des coups joués:
        1. Parcourt l'historique en sens inverse
        2. Pour chaque transition (s,s'), met à jour V(s) avec:
        V(s) = V(s) + learning_rate * (V(s') - V(s))
        3. Vide l'historique une fois l'apprentissage terminé
        """
        print(self.historique)
        self.historique.reverse()
        for s,ss in self.historique:
            if s not in self.v_function:
                    self.v_function[s] = 0
            if ss not in self.v_function:
                    self.v_function[ss] = 0

            self.v_function[s] = self.v_function[s] + self.lr * (self.v_function[ss]-self.v_function[s])
        self.historique.clear()

    def next_epsilon(self,coef=0.95, min=0.05):
        """
        Réduit progressivement l'exploration au profit de l'exploitation.
        
        Args:
            coef (float): Facteur de réduction d'epsilon (0.95 par défaut)
            min (float): Valeur minimale d'epsilon (0.05 par défaut)
            
        Exemple:
            Si epsilon = 0.9 et coef = 0.95
            Nouveau epsilon = max(0.9 * 0.95, 0.05) = 0.855
        """
        self.eps = self.eps * coef
        if self.eps < min:
            self.eps = min
