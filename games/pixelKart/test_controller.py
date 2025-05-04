from game_models.kart import humanKart, kart
from game_controller import GameController

if __name__ == "__main__":
   

    human = humanKart ("Humain", 12, 20)
    human2 = humanKart ("Bob", 12, 20)
    random = kart("BipBoup", 12, 20)

    game_controller = GameController(human, human2, 'Large')
    game_controller.start()
    