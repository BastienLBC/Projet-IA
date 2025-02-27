"""
Module qui gère les actions du joueur,
et fait les liens entre les deux modèles game_view et game_model
"""
from Players.players import *
from Game.game_model import *
from Game.game_view import *
from Players.players import *

class GameControler:
    """
    Controleur des alumettes, gère la logique 

    Attributes : 
        model : instance de game_model
        view : instance de game_view
    """
    def __init__(self, players: list[str], nb_torchs:int=15):
        """
        Initialise le controleur
        
        Args:
            players (list): liste des joueurs
            nb_matchs (int): nombres d'alumettes
        Raise: 
            ValueError : si il n'y a pas au moins un joueur humain
        """
        """
        if not isinstance(players[0], Human) and not isinstance(players[1], Human):
            raise ValueError("Il doit y avoir au moins un joueur humain.")
        """
        self.model = GameModel(nb_torchs, players)
        self.view = GameView(self)

        if self.is_ai_player():
            self.handle_ai_move()

    def start(self)-> None:
        """
        Lance le jeu
        """
        self.view.mainloop()

    def get_nb_torchs(self)-> int:
        """
        Retourne le nombre de torches en jeu

        Returns:
            int: le nombre d'alumettes restantes
        """
        return self.model.nb

    def get_status_message(self)-> str:
        """
        Retourne le message à afficher, entre le le joueur du tour et le joueur qui a gagné

        Returns:
            string:
                -"{joueur} a gagné", si la partie est terminée
                -"Au tour du grand {joueur}" sinon
        """
        if self.model.is_game_over():
            return f"{self.model.get_winner().name} a gagné !"
        return f"Au tour du grand : {self.model.get_current_player().name}"

    def reset_game(self)->None:
        """
        Réinitialise tout, le model, l'interface graphique,
        et déclenche un coup du bot si le nouveau joueur courant n'est pas human
        """
        self.model.reset()
        self.view.reset()
        if self.is_ai_player():
            self.handle_ai_move()

    def handle_human_move(self, count: int)->None:
        """
        gère le choix de l'humain, retire le nombre d'alumette choisi.
        Si la partie n'est pas finie, et que le joueur suivant est un bot,
        alors elle joue le coup du bot et met à jour l'interface

        Args:
            int: le nombre d'alumettes
        """
        if isinstance(self.model.get_current_player(), Human):
            self.model.step(count)
            if self.model.is_game_over():
                self.handle_end_game()
            else:
                self.model.switch_player()
                if self.is_ai_player():
                    self.handle_ai_move()
            self.view.update_view()

    def handle_ai_move(self)->None:
        """
        Gère le choix de l'ia, retire le nombre d'alumettes de l'ia,
        et passe au joueur suivant / vérifie si la partie est finie
        """
        action = self.model.get_current_player().play()
        self.model.step(action)
        if self.model.is_game_over():
            self.handle_end_game()
        else:
            self.model.switch_player()
        self.view.update_view()

    def handle_end_game(self)->None:
        """
        Fin du jeu, assigne le gagnant et le perdant
        """
        winner = self.model.get_winner()
        winner.win()
        loser = self.model.get_loser()
        loser.lose()
        self.view.end_game()

    def is_ai_player(self)->bool:
        """
        Vérifie si le joueur est un bot

        returns :
            -bool: true : le joueur est un bot
        """
        is_player = isinstance(self.model.get_current_player(), Player)
        is_human = isinstance(self.model.get_current_player(), Human)
        return is_player and not is_human

    def training(self, ai1, ai2, nb_games, nb_epsilon):
        # Train the AIs @ai1 and @ai2 during @nb_games games
        # epsilon decrease every @nb_epsilon games
        training_game = GameModel(15, players=[ai1, ai2], display=False)
        for i in range(0, nb_games):
            if i % nb_epsilon == 0:
                ai1.next_epsilon()
                ai2.next_epsilon()

            training_game.play()
            ai1.train()
            ai2.train()

            training_game.reset()

    