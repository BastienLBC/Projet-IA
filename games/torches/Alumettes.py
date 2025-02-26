from Game.game_controller import *
from Players.players import *

if __name__ == "__main__":
    p1 = Human('test')
    p2 = Human("zigzze")
    
    game = GameControler([p1, p2])
    game.start()