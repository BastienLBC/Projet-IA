# python
import sys
from games.pixelKart.pixel_kart_game import PixelKartGame


def main():
    if len(sys.argv) > 3:
        circuit_name = sys.argv[1]
        laps = int(sys.argv[2])
        mode = sys.argv[3]
    else:
        raise ValueError("Choisissez un circuit, le nombre de tours et un mode de jeu.")

    game = PixelKartGame(circuit_name, laps, mode)
    game.setup()
    game.run()


if __name__ == "__main__":
    main()