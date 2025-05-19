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
        self.model.reset_game()
        self.view.reset()
        if self.is_random_player():
            self.handle_random_moove()

    def start_random_move(self) -> None:
        if self.is_random_player():
            self.view.after(500, self.handle_random_moove)

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
        if self.model.is_finish():
            return f"{self.model.get_winner().name} a gagné !"

    def handle_player_moove(self, bind: str) -> None:
        if isinstance(self.model.get_current_player(), humanKart):
            human_player = self.model.get_current_player()
            human_player.Event = bind  # Stocke la touche
            self.model.moove(bind)
            if self.model.is_finish():
                self.handle_end_game()
            else:
                self.model.switch_player()
                self.view.update_view()
                self.start_random_move()

    def handle_random_moove(self) -> None:
        move = self.model.get_current_player().play()  # Choisit un bind aléatoire
        self.model.one_action(move)  # Applique l'action via one_action
        if self.model.is_finish():
            self.handle_end_game()
        else:
            self.model.switch_player()
        self.view.update_view()

    def handle_end_game(self) -> None:
        winner = self.model.get_winner()
        loser = self.model.get_loser()
        if winner:
            winner.win()
        if loser:
            loser.lose()
        self.view.end_game()
