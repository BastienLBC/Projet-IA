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
    ui = ia_player('ui')

    test= ia_player('test')
    jsp = Human('jsp')

    """

    training(joueur, test, 1000, 10)

    compare_ai (test)
    
    
    GameControler(jsp, test).start()

    compare_ai(test)
    
    """
    training(bob, alice, 100000 , 10)
    training(randy,joueur, 100000 , 10)

    bob.wins = 0
    bob.losses = 0
    
    print("test1")

    training(bob,joueur, 100000 , 10)
    compare_ai(bob, alice, randy)

    alice.download(alice)
    ui.upload(ui)

    

    """"
    print("test2")
    training(bob,joueur, 1000000, 10)
    training(alice,joueur, 1000000, 10)
    training(randy,joueur, 1000000, 10)

   
    
    GameControler(bob,jsp).start()
    GameControler(alice,jsp).start()
    """
    
    
