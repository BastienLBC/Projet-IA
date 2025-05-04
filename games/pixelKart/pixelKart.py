import sys
from games.pixelKart.pixel_kart_game import PixelKartGame

def main():
    if len(sys.argv) > 1:
        circuit_name = sys.argv[1]
    else:
        raise ValueError("Aucun circuit sélectionné. Veuillez en choisir un dans le launcher.")

    game = PixelKartGame(circuit_name)
    game.setup()
    game.run()

if __name__ == "__main__":
    main()