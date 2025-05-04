from game_models.kart import humanKart, kart
from game_controller import GameController


if __name__ == "__main__":
   

    human = humanKart ("Humain")
    human2 = humanKart ("Bob")
    random = kart("BipBoup")

    game_controller = GameController(human, human2, 'Large')
    game_controller.start()
    