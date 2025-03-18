from games.Cube.game_Model.game_model import GameModel
from games.Cube.game_controller import GameController
from games.Cube.game_view import GameView
from games.Cube.game_Model.players import Player

def test_display():
    # Créez deux joueurs
    player1 = Player(name="Player 1", color="green")
    player2 = Player(name="Player 2", color="lightgray")

    # Initialisez le contrôleur avec les joueurs
    controller = GameController(player1, player2)

    # Démarrez le jeu pour tester l'affichage
    controller.start()

if __name__ == "__main__":
    test_display()