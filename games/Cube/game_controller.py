from games.Cube.game_Model.game_model import GameModel
from games.Cube.game_Model.players import Player
from games.Cube.game_view import GameView

class GameController:
    def __init__(self, player1, player2) -> None:
        self.model = GameModel(player1, player2)
        self.view = GameView(self)

        if self.is_random_player():
            self.handle_random_moove()

    def start(self) -> None:
        self.view.mainloop()

    def reset_game(self) -> None:
        self.model = GameModel(self.model.players1, self.model.players2)
        self.view.reset()
        if self.is_random_player():
            self.handle_random_moove()

    def is_random_player(self) -> bool:
        return isinstance(self.model.get_current_player(), Player) and self.model.get_current_player().name == "Bot"

    def get_status_message(self) -> str:
        if self.model.is_finished():
            return f"{self.model.get_winner().name} a gagné !"
        return f"Au tour du grand : {self.model.get_current_player().name}"

    def handle_player_moove(self, bind: str) -> None:
        if isinstance(self.model.get_current_player(), Player):
            self.model.moove(bind)
            if self.model.is_finished():
                self.handle_end_game()
            else:
                self.model.switch_player()
                if self.is_random_player():
                    self.handle_random_moove()
            self.view.update_view()

    def handle_random_moove(self) -> None:
        moove = self.model.get_current_player().play()
        self.model.moove(moove)
        if self.model.is_finished():
            self.handle_end_game()
        else:
            self.model.switch_player()
        self.view.update_view()

    def handle_end_game(self) -> None:
        winner = self.model.get_winner()
        winner.win()
        loser = self.model.get_looser()
        loser.lose()
        self.view.end_game()