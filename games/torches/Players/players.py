"""
Module qui gère les différents types de joueurs
"""
import random

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
    def __init__(self, name: str, game=None, epsilon : float=0.9 ,learning_rate : float=0.01,historique: list[int] = None, previous_state: int = None) -> None:
        super().__init__(name,game)
        self.eps= epsilon
        self.lr = learning_rate
        self.historique =  historique if historique is not None else []
        self.previous_state = previous_state
        self.v_function = {"lose":-1, "win":1}
    def get_nb_torchs(self) -> int:
        """
        Retourne le nombre actuel d'allumettes en jeu.
        """
        return self.game.nb 
    
    def exploit(self) -> int:
        """
        Choisit la pire action possible pour le donner a son adversaire
        """
        best_move = None
        best_value = float("-inf") 

        nb_torches = self.get_nb_torchs()
        for i in [1,2,3]:
           next_state = nb_torches - i
           next_value = self.v_function.get(next_state, 0)

           if  next_value > best_value :
               best_value = next_value
               best_move = i

        return best_move
    
    def play(self) -> int:
        """
        Ajoute la transition des coups à l'historique,
        en fonction de l'epsilon, joue soit un nb aleatoire,
        soit le coup réfléchi par l'exploitation.
        met à jour l'état précédent
        
        Returns:
            -Int : le coup à jouer choisi par l'ia
        """
        current_state = self.get_nb_torchs()

        if self.previous_state is not None:
            self.historique.append((self.previous_state, self.get_nb_torchs()))

        if random.uniform(0,1.0) < self.eps:
            move = random.randint(1,3)
        else:
            move = self.exploit()

        self.previous_state = current_state
        return move
    
    def win(self) -> None:
        """
        Ajoute une victoire à l'ia, et met à jour la transition
        """
        super().win()
        self.historique.append((self.previous_state, self.v_function["win"]))
        self.previous_state = None
        self.train()

    def lose(self) -> None:
        """
        Ajoute une défaite à l'ia, et met à jour la transition
        """
        super().lose()
        self.historique.append((self.previous_state, self.v_function["lose"]))
        self.previous_state = None
        self.train()

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
            self.v_function[state] += self.lr * float(self.v_function[next_state] - self.v_function[state])

    def next_epsilon(self, coef: float = 0.95, min: float = 0.05) -> None:
        """
        Réduit l'epsilon pour favoriser l'exploitation au fil du temps.
        L'epsilon ne descend jamais en dessous du minimum spécifié.
        """
        self.eps = max(self.eps * coef, min)

    