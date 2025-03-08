from Game.game_controller import *

if __name__ == "__main__":
    noob = Player("noob")
    alice = Ai_player("Alice")
    bob = Ai_player("Bob")
    randy = Ai_player("Randy")

    GameController.training(alice,randy,100000,10)
    GameController.compare_ai(alice,randy)
