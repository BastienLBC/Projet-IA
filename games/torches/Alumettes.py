from Game.game_controller import *

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

    test= ia_player('test')
    jsp = Human('jsp')
    """
    training(bob, alice, 100000 , 10)
    training(randy,joueur, 100000 , 10)

    bob.wins = 0
    bob.losses = 0

    print("test1")

    training(bob,joueur, 100000 , 10)
    compare_ai(bob, alice, randy)
    """
    """
    alice.upload()
    """
    # After 10.000.000 games, the states have been saved with upload, so please don't touch it. You can use download to recover the states.
    test.download()
    GameControler(test, jsp).start()
