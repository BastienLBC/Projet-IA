"""
Module qui gère les différents types de joueurs
"""
from Game.game_model.game_model import *
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
        self.v_function = {"lose":-10, "win":10}
    def get_nb_torchs(self) -> int:
        """
        Retourne le nombre actuel d'allumettes en jeu.
        """
        return self.game.nb 
    
    def exploit(self) -> int:
        """
        Choisit la pire action possible pour donner la pire situation à son adversaire.
        """
        best_move = None
        worst_value = float("inf") 

        nb_torches = self.get_nb_torchs()
        for i in [1, 2, 3]:
            next_state = nb_torches - i
            next_value = self.v_function.get(next_state, 0)

            if next_value < worst_value:
                worst_value = next_value
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
            self.historique.append((self.previous_state, current_state))

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
        self.historique.append((self.previous_state,"win"))
        self.previous_state = None
        self.train()

    def lose(self) -> None:
        """
        Ajoute une défaite à l'ia, et met à jour la transition
        """
        super().lose()
        self.historique.append((self.previous_state, "lose"))
        self.previous_state = None
        self.train()

    def train(self) -> None:
        """
        Entraîne l'IA en se basant sur l'historique.
        Parcourt l'historique à l'envers et le vide une fois terminé.
        """
        while self.historique:
            previous_state, current_state = self.historique.pop()
            if previous_state not in self.v_function:
                self.v_function[previous_state] = 0
    
            self.v_function[previous_state] += self.lr * (self.v_function.get(current_state) - self.v_function[previous_state])
            
    def next_epsilon(self, coef: float = 0.95, min: float = 0.05) -> None:
        """
        Réduit l'epsilon pour favoriser l'exploitation au fil du temps.
        L'epsilon ne descend jamais en dessous du minimum spécifié.
        """
        self.eps = self.eps * coef
        if self.eps < min:
            self.eps = min

    def is_ai_player(self)->bool:
        """
        Vérifie si le joueur est un bot

        returns :
            -bool: true : le joueur est un bot
        """
        is_player = isinstance(self.model.get_current_player(), Player)
        is_human = isinstance(self.model.get_current_player(), Human)
        return is_player and not is_human

    def training(ai1, ai2, nb_games, nb_epsilon):
        # Train the AIs @ai1 and @ai2 during @nb_games games
        # epsilon decrease every @nb_epsilon games
        training_game = GameModel(15, ai1, ai2, display= False)
        for i in range(0, nb_games):
            if i % nb_epsilon == 0:
                if type(ai1)==ia_player : ai1.next_epsilon()
                if type(ai2)==ia_player : ai2.next_epsilon()

            training_game.play()
            if type(ai1)==ia_player : ai1.train()
            if type(ai2)==ia_player : ai2.train()

            training_game.reset()

    def compare_ai(*ais):
        # Print a comparison between the @ais
        names = f"{'':4}"
        stats1 = f"{'':4}"
        stats2 = f"{'':4}"

        for ia_player in ais :
            names += f"{ia_player.name:^15}"
            stats1 += f"{str(ia_player.wins)+'/'+str(ia_player.nb_games):^15}"
            stats2 += f"{f'{ia_player.wins/ia_player.nb_games*100:4.4}'+'%':^15}"

        print(names)
        print(stats1)
        print(stats2)
        print(f"{'-'*4}{'-'*len(ais)*15}")

        all_v_dict = {key : [ia_player.v_function.get(key,0) for ia_player in ais] for key in ais[0].v_function.keys()}
        sorted_v = lambda v_dict : sorted(filter(lambda x : type(x[0])==int ,v_dict.items()))
        for state, values in sorted_v(all_v_dict):
            print(f"{state:2} :", end='')
            for value in values:
                print(f"{value:^15.3f}", end='')
            print()
    def upload(self, filename="ai_state.txt"):
        """Enregistre les valeurs de l'état"""
        with open(filename, "w") as file:
            sorted_v = sorted(filter(lambda x: isinstance(x[0], int), self.v_function.items()))
            for state, value in sorted_v:
                file.write(f"{state}: {value:.10f}\n")

    def download(self, filename="ai_state.txt"):
        """
        Charge les valeurs de l'état
        """ 
        with open(filename, "r") as file:
            for line in file:
                state, value = line.strip().split(": ")
                self.v_function[int(state)] = float(value)
            self.eps = 0.05