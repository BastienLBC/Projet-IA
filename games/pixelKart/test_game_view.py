import customtkinter as ctk
from game_view import GameView
from kart import kart
import circuit
import pixelKart_dao as dao

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    player1 = kart(name="Player1", x=1, y=1, speed=1)
    player2 = kart(name="Player2", x=3, y=3, speed=2)

    controller = circuit.Circuit(12, 20, player1.name, player2.name)

    circuit_rows = 12
    circuit_cols = 20

    game_view = GameView(controller, circuit_rows, circuit_cols)

    circuit_data = dao.get_by_name("Petit")
    karts_data = {(4, 4): "red", (3, 3): "blue"}

    game_view.update_player_info(player1, player2, laps_remaining=3)
    game_view.update_view(circuit_data, karts_data)

    # Lancement de l'interface
    game_view.mainloop()

if __name__ == "__main__":
    main()