from Game.game_controller import *

# if __name__ == "__main__":
#     p1 = Human('test')
#     p2 = Human("zigzze")
    
#     game = GameControler([p1, p2])
#     game.start()

if __name__ == "__main__":
    noob = Player('noob')
    alice = ai_player('Alice')
    bob = ai_player('Bob')
    randy = ai_player('Randy')


GameControler.training(alice,bob, 1000, 10)
GameControler.compare_ai(alice,bob)

GameControler.training(randy, noob, 1000, 10)
GameControler.compare_ai(randy,noob)

bob.wins = 0
bob.losses = 0

GameControler.training(bob, noob, 1000, 10)
GameControler.compare_ai(alice, bob, randy)
GameControler.training(bob, noob, 100000, 10)
GameControler.compare_ai(alice, bob, randy)
