from Game.dao import init_db
from Game.game_models.players import AiPlayer, HumanPlayer, Player
from Game.game_controller import GameController

if __name__ == "__main__":
    init_db()

    human = HumanPlayer("Humain", "green")
    ai1 = AiPlayer("IA1", "blue")
    ai2 = AiPlayer("IA2", "red")
    random = Player("Random", "black")

    board_size = 3
    game_controller = GameController(human, ai2, board_size)
    
    game_controller.training(ai1, ai2, board_size,800000, epsilon=10)
    GameController.compare_ai(ai2)
    ai2.wins = 0
    ai2.loses = 0
    
    
    game_controller.training(random,ai2,board_size,300 , epsilon=0.1)
    game_controller.compare_ai(ai2)