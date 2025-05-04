import sys
import customtkinter as ctk
from games.pixelKart.game_view import GameView
from games.pixelKart.game_models.kart import kart, humanKart
import games.pixelKart.pixelKart_dao as dao
import games.pixelKart.game_models.circuit as circuit

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    # Récupérer le circuit depuis les arguments
    if len(sys.argv) > 1:
        circuit_name = sys.argv[1]
    else:
        raise ValueError("Aucun circuit sélectionné. Veuillez en choisir un dans le launcher.")

    circuit_data = dao.get_by_name(circuit_name)
    if not circuit_data:
        raise ValueError(f"Le circuit '{circuit_name}' est introuvable dans le fichier circuits.txt.")

    player1 = humanKart(name="Player1")
    player2 = kart(name="Player2")

    controller = circuit.Circuit(player1, player2, gp=circuit_data)
    controller.start()

    circuit_rows = 12
    circuit_cols = 20

    game_view = GameView(controller, circuit_rows, circuit_cols)

    karts_data = controller.get_karts_positions()
    game_view.update_player_info(player1, player2, laps_remaining=controller.nb_laps)
    game_view.update_view(circuit_data, karts_data)

    game_view.mainloop()

if __name__ == "__main__":
    main()