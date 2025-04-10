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
    
    game_controller.training(ai1, ai2, board_size,1000, epsilon=10)
    GameController.compare_ai(ai2)
    
