from Game.dao import init_db
from Game.game_controller import GameController

if __name__ == "__main__":
    init_db()

    human = HumanPlayer("Humain", "green")
    ai1 = AiPlayer("IA1", "blue")
    ai2 = AiPlayer("IA2", "red")
    random = Player("Random", "black")

    board_size = 3
    
    
    GameController.training(ai1, ai2, board_size, 500000,1000)
    GameController.compare_ai(ai2)
    
    ai2.losses = 0
    ai2.wins = 0
    ai2.eps = 0.0
        
    GameController.training(random,ai2,board_size, 1000)
    GameController.compare_ai(ai2)
    
    
    