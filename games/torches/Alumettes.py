from Game.game_controller import *
from Players.players import *



def training(ai1, ai2, nb_games, nb_epsilon):
        # Train the AIs @ai1 and @ai2 during @nb_games games
        # epsilon decrease every @nb_epsilon games
        training_game = GameModel(15, ai1, ai2, displayable = False)
        for i in range(0, nb_games):
            if i % nb_epsilon == 0:
                if type(ai1)==ia_player : ai1.next_epsilon()
                if type(ai2)==ia_player : ai2.next_epsilon()

            training_game.play()
            if type(ai1)==ia_player : ai1.train()
            if type(ai2)==ia_player : ai2.train()

            training_game.reset()

if __name__ == "__main__":
    
    """
    p1 = Human('test')
    p2 = Human("zigzze")
    
    game = GameControler(p1, p2)
    game.start()
    """

    
    joueur = Player('basique')
    alice = ia_player('Alice')
    bob = ia_player('Bob')
    randy = ia_player('Randy')

    

    game = GameControler(bob, alice)
    game.training(bob, alice, 1000, 10)

    jsp = GameControler(randy, joueur)
    jsp = jsp.training(randy,joueur,1000,10)
    
    
