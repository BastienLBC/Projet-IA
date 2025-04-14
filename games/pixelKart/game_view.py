import customtkinter as ctk
from pixelKart_circuitFrames import CircuitRaceFrame


class GameView(ctk.CTk):
    """Gère la vue du jeu PixelKart"""

    def __init__(self, controller) -> None:
        """
        Initialise la fenêtre principale du jeu
        Args:
            controller: Instance du contrôleur du jeu
        """
        super().__init__()
        self.controller = controller

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.title("PixelKart")
        self.minsize(800, 500)
        self.maxsize(800, 500)

        self.message_label = ctk.CTkLabel(
            self,
            text="",
            font=("OCR A Extended", 20, "bold"),
            text_color="#32CD32",
            padx=30
        )
        self.message_label.pack(pady=20)

        self.game_frame = CircuitRaceFrame(self)
        self.game_frame.configure()
        self.game_frame.pack(pady=10)

        self.bind_all("<Key>", self.on_key_press)

        self.reset_button = ctk.CTkButton(
            self,
            text="Recommencer",
            command=self.controller.reset_game
        )
        self.reset_button.pack_forget()

    def on_key_press(self, event):
        """
        Gère les événements clavier
        """
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
        self.controller.handle_action(bind)

    def update_view(self, circuit, karts):
        """
        Met à jour l'affichage du circuit et des karts
        Args:
            circuit: État actuel du circuit
            karts: Dictionnaire des positions et couleurs des karts
        """
        if circuit:
            self.game_frame.dto_to_grid(circuit)
        if karts:
            self.game_frame.update_view(karts)

    def show_message(self, message):
        """
        Affiche un message dans le label
        """
        self.message_label.configure(text=message)

    def show_reset_button(self):
        """
        Affiche le bouton reset
        """
        self.reset_button.pack(pady=10)

    def hide_reset_button(self):
        """
        Cache le bouton reset
        """
        self.reset_button.pack_forget()

#pour tester l'affichage
# if __name__ == "__main__":
#     # Classe Mock pour tester l'affichage
#     class MockController:
#         def reset_game(self):
#             pass
#
#         def handle_action(self, action):
#             print(f"Action: {action}")
#
#
#     # Créer la vue avec le mock controller
#     view = GameView(MockController())
#
#     # Exemple de circuit basique
#     basic_circuit = "GGGGGGGGWGGGGGGGGGGG,GGGRRRRRFRRRRRRRRGGG,GGRRRRRRFRRRRRRRRRGG,GRRRRRRRFRRRRRRRRRRG,GRRRRRGGWGGGGGGRRRRG,GRRRRGWWWWWWWWWGRRRG,GRRRRRGGGGGGGGGRRRRG,GRRRRRRRRRRRRRRRRRRG,GRRRRRRRRRRRRRRRRRRG,GGRRRRRRRRRRRRRRRRGG,GGGRRRRRRRRRRRRRRGGG,GGGGGGGGGGGGGGGGGGGG"
#
#     # Exemple de karts sur le circuit
#     karts = {
#         (1, 1): "red",  # Position et couleur du kart 1
#         (2, 2): "blue"  # Position et couleur du kart 2
#     }
#     # Mettre à jour la vue avec les données
#     view.update_view(basic_circuit, karts)
#
#     # Lancer l'application
#     view.mainloop()