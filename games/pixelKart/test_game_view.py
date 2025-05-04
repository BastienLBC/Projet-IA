import customtkinter as ctk
from game_view import GameView
from game_models.kart import kart
import game_models.circuit as circuit
import i.pixelKart_dao as dao

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    player1 = kart(name="Player1", x=1, y=1, speed=1)
    player2 = kart(name="Player2", x=3, y=3, speed=2)

    circuit_data = dao.get_by_name("Petit")
    if not circuit_data:
        raise ValueError("Le circuit 'Petit' est introuvable dans le fichier circuits.txt.")

    controller = circuit.Circuit(12, 20, player1, player2, gp=circuit_data)

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