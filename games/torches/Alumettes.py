from Game.game_controller import *
from Players.players import *

if __name__ == "__main__":
    """"
    p1 = Human('test')
    p2 = Human("zigzze")
    
    game = GameControler([p1, p2])
    game.start()
    """

    joueur = Player('basique')
    alice = ia_player('Alice')
    bob = ia_player('Bob')
    randy = ia_player('Randy')

    
    game = GameControler([bob, alice])
    game.training(bob,alice,1000,10)

    jsp = GameControler([randy, joueur])
    jsp = jsp.training(randy,joueur,1000,10)

    
