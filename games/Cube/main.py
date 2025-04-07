from Game.dao import init_db
from Game.game_models.players import AiPlayer, HumanPlayer
from games.Cube.Game.game_controller import GameController

if __name__ == "__main__":
    init_db()

    human = HumanPlayer("Humain", "green")
    ai2 = AiPlayer("IA2", "red", learning_rate=0.1, gamma=0.9, epsilon=0.9)

    board_size = 6
    game_controller = GameController(human, ai2, board_size)
    game_controller.start()
    GameController.compare_ai(ai2)