from games.pixelKart.game_models.circuit import *
from games.pixelKart.game_models.kart import *
from games.pixelKart.game_view import *

class GameController:

    def __init__(self, player1: kart, player2: kart, circuit: str):
        """
        Initialise le contrôleur de jeu avec les joueurs et le circuit.
        Utilise 'Basic' si le circuit demandé n'existe pas.
        """

        self.model = Circuit(player1, player2, circuit)
        self.view = GameView(self)

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
        return not isinstance(self.model.get_current_player(), humanKart)

    def get_status_message(self)-> str:
        """
        Retourne le message à afficher, entre le le joueur du tour et le joueur qui a gagné

        Returns:
            string:
                -"{joueur} a gagné", si la partie est terminée
                -"Au tour du grand {joueur}" sinon
        """
        if self.model.is_finished():
            return f"{self.model.get_winner().name} a gagné !"

    def handle_player_moove(self, bind:str)->None:
        """
        Fais le moove du joueur avec le bind reçu en paramètre,
        qui déplace le joueur de case

        """
        if isinstance(self.model.get_current_player(), humanKart): #à retirer si pas de classe ia
            human_player = self.model.get_current_player()
            human_player.Event = bind  # Stocke la touche

            self.model.moove(bind)  # Déplace selon la touche reçue
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
            if self.model.is_finished():
                self.handle_end_game()
            else:
                self.model.switch_player()
            self.view.update_view()

    def handle_end_game(self)->None:
        """
        Fin du jeu, assigne le gagnant et le perdant
        """
        winner = self.model.get_winner()
        loser = self.model.get_loser()
        self.view.end_game()
