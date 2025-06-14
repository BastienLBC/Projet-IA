from Game.dao import init_db
from Game.game_models.players import AiPlayer, HumanPlayer
from Game.game_controller import GameController

if __name__ == "__main__":
    init_db()

    
    ai1 = AiPlayer(name="IA_1", color="blue", learning_rate=0.01, gamma=10, epsilon=0.9)
    ai2 = AiPlayer(name="IA_2", color="red", learning_rate=0.01, gamma=10, epsilon=0.9)
    human = HumanPlayer(name="Joueur 1", color="green")

    board_size = 4
    # nb_games = 20000
    # eps = 400
    #
    # GameController.training(ai1, ai2, board_size, nb_games, eps)
    # print("------------------------------------------------------------")
    #
    # GameController.compare_ai(ai1, ai2)
    
    
    ai2.epsilon = 0.05
    ai2.upload("store3.db")
    game = GameController(human, ai2, board_size)
    game.start()
    
