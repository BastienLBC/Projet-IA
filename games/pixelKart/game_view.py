import customtkinter as ctk
from games.pixelKart.pixelKart_circuitFrames import CircuitRaceFrame

class GameView(ctk.CTk):
    """Gère la vue du jeu PixelKart"""

    def __init__(self, controller, circuit_rows, circuit_cols) -> None:
        super().__init__()
        self.controller = controller

        cell_size = 20
        width = circuit_cols * cell_size + 300
        height = circuit_rows * cell_size
        self.geometry(f"{width}x{height}")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.title("PixelKart")

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        self.game_frame = CircuitRaceFrame(main_frame, rows=circuit_rows, cols=circuit_cols)
        self.game_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        info_frame = ctk.CTkFrame(main_frame, width=300)
        info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.info_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=("OCR A Extended", 14),
            text_color="white",
            padx=10
        )
        self.info_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.bind_all("<Key>", self.on_key_press)

        self.reset_button = ctk.CTkButton(
            info_frame,
            text="Recommencer",
            command=self.controller.reset_game
        )
        self.reset_button.pack(pady=10)

        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

    def update_player_info(self, player1, player2, laps_remaining):
        """
        Met à jour les informations des joueurs et les tours restants.
        """
        info_text = (
            f"Nombre de tours restants : {laps_remaining}\n\n"
            f"Joueur 1 ({player1.name}):\n"
            f"  Position: ({player1.x}, {player1.y})\n"
            f"  Direction: {player1.direction}\n"
            f"  Vitesse: {player1.speed}\n"
            f"  Tours effectués: {player1.laps}\n"
            f"  En vie: {'Oui' if player1.inLife else 'Non'}\n\n"
            f"Joueur 2 ({player2.name}):\n"
            f"  Position: ({player2.x}, {player2.y})\n"
            f"  Direction: {player2.direction}\n"
            f"  Vitesse: {player2.speed}\n"
            f"  Tours effectués: {player2.laps}\n"
            f"  En vie: {'Oui' if player2.inLife else 'Non'}"
        )
        self.info_label.configure(text=info_text)

    def on_key_press(self, event):
        """
        Gère les événements clavier
        """
        if not self.controller.current_player:
            print("Erreur : Aucun joueur actuel défini.")
            return

        bind = event.keysym.upper()
        if bind == "Z":
            bind = "Accelerate"
        elif bind == "S":
            bind = "Decelerate"
        elif bind == "Q":
            bind = "Left"
        elif bind == "D":
            bind = "Right"
        elif bind == "SPACE":
            bind = "Nothing"
        self.controller.one_action(bind)

        if not self.controller.is_finish():
            self.controller.switch_player()
            ai_move = self.controller.current_player.play()
            self.controller.one_action(ai_move)
            if not self.controller.is_finish():
                self.controller.switch_player()

        karts_data = self.controller.get_karts_positions()
        self.update_player_info(self.controller.player1, self.controller.player2,
                                laps_remaining=self.controller.nb_laps)
        self.update_view(self.controller.circuit, karts_data)

    def update_view(self, circuit, karts):
        """
        Met à jour l'affichage du circuit et des karts
        """
        if circuit:
            self.game_frame.dto_to_grid(circuit)
        if karts:
            self.game_frame.update_view(karts)

    def reset(self):
        self.game_frame.dto_to_grid(self.controller.circuit)
        karts_data = self.controller.get_karts_positions()
        self.game_frame.update_view(karts_data)
        self.info_label.configure(text="")