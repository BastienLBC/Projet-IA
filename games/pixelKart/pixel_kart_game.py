import customtkinter as ctk
from games.pixelKart.game_view import GameView
from games.pixelKart.game_models.kart import kart, humanKart
import games.pixelKart.pixelKart_dao as dao
import games.pixelKart.game_models.circuit as circuit

class PixelKartGame:
    def __init__(self, circuit_name, laps, mode):
        self.circuit_name = circuit_name
        self.laps = laps
        self.mode = mode
        self.controller = None
        self.game_view = None

    def setup(self):
        circuit_data = dao.get_by_name(self.circuit_name)
        if not circuit_data:
            raise ValueError(f"Le circuit '{self.circuit_name}' est introuvable dans le fichier circuits.txt.")

        player1 = humanKart(name="Player1")
        player2 = kart(name="Player2")

        self.controller = circuit.Circuit(player1, player2, gp=circuit_data)
        self.controller.nb_laps = self.laps
        self.controller.start()

        circuit_rows = 12
        circuit_cols = 20

        self.game_view = GameView(self.controller, circuit_rows, circuit_cols)
        karts_data = self.controller.get_karts_positions()
        self.game_view.update_player_info(player1, player2, laps_remaining=self.controller.nb_laps)
        self.game_view.update_view(circuit_data, karts_data)

    def run(self):
        if not self.controller or not self.game_view:
            raise RuntimeError("Le jeu n'est pas configuré. Appelez d'abord la méthode setup().")
        self.game_view.mainloop()