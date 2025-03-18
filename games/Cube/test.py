from games.Cube.game_Model.game_model import GameModel
from games.Cube.game_controller import GameController
from games.Cube.game_view import GameView
from games.Cube.game_Model.players import Player

def test_display():
    player1 = Player(name="Player 1", color="red")
    player2 = Player(name="Player 2", color="blue")

    controller = GameController(player1, player2)

    controller.start()

if __name__ == "__main__":
    test_display()