from Game.dao import init_db
from Game.game_models.players import AiPlayer, HumanPlayer
from Game.game_controller import GameController

if __name__ == "__main__":
    init_db()

    # Création des IA
    ai1 = AiPlayer(name="IA_1", color="blue", learning_rate=0.01, gamma=0.9, epsilon=0.9)
    ai2 = AiPlayer(name="IA_2", color="red", learning_rate=0.01, gamma=0.9, epsilon=0.9)

    board_size = 6
    nb_games = 100
    eps = 10

    GameController.training(ai1, ai2, board_size, nb_games, eps)
    print("------------------------------------------------------------")
    GameController.compare_ai(ai1, ai2)
