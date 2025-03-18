"""
Module qui gère les actions du joueur,
et fait les liens entre les deux modèles game_view et game_model.py
"""
from game_Model.game_model import *
from game_Model.players import *
from game_view import *

import random

class GameController:
    """
    Controleur de Cubee, gère la logique

    Attributes :
        model : instance de game_model.py
        view : instance de game_view
    """
    def __init__(self, player1, player2)->None:
        """
        Initialise le constructeur
        """
        self.model = GameModel(player1, player2)
        self.view = GameView(self)

        if self.is_random_player():
            self.handle_random_moove()

    def start(self)->None:
        """
        Lance le jeu
        """
        self.view.mainloop()

    def  reset_game(self)->None:
        """
        Réinitialise tout, le model, l'interface graphique,
        et déclenche un coup du bot si le nouveau joueur courant n'est pas Player
        """
        self.model.reset()
        self.view.reset()
        if self.is_random_player():
            self.handle_random_moove()

    def is_random_player(self)->bool:
        """
        Vérifie si le joueur est un bot

        returns :
            -bool: true : le joueur est un bot
        """
        return isinstance(self.model.get_current_player(), random)

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

    def handle_player_moove(self, bind:str)->None:
        """
        Fais le moove du joueur avec le bind reçu en paramètre,
        qui déplace le joueur de case

        """
        if isinstance(self.model.get_current_player(), Player): #à retirer si pas de classe ia
            self.model.moove(bind)
            if self.model.is_finished():
                self.handle_end_game()
            else:
                self.model.switch_player()
                if self.is_random_player():
                    self.handle_random_moove()
            self.view.update_view()

    def handle_random_moove(self)->None:
        """
        Fais le moove de l'ia avec un bind random
        qui déplace le random player de case
        """
        moove = self.model.get_current_player().play() #choisi un bind random
        self.model.moove(moove)
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
