import customtkinter as ctk
from Game.game_controller import *


class GameConfig:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Configuration du jeu d'allumettes")
        self.window.geometry("600x400")

        # Mode de jeu
        self.mode_frame = ctk.CTkFrame(self.window)
        self.mode_frame.pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(self.mode_frame, text="Mode de jeu", font=("Arial", 16, "bold")).pack()

        self.mode = ctk.StringVar(value="ia")
        ctk.CTkRadioButton(self.mode_frame, text="Contre l'IA", variable=self.mode, value="ia").pack(pady=5)
        ctk.CTkRadioButton(self.mode_frame, text="Joueur contre Joueur", variable=self.mode, value="pvp").pack(pady=5)

        # Configuration IA
        self.ia_frame = ctk.CTkFrame(self.window)
        self.ia_frame.pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(self.ia_frame, text="Configuration IA", font=("Arial", 16, "bold")).pack()

        self.ia_type = ctk.StringVar(value="trained")
        ctk.CTkRadioButton(self.ia_frame, text="IA entraînée", variable=self.ia_type, value="trained").pack(pady=5)
        ctk.CTkRadioButton(self.ia_frame, text="IA aléatoire", variable=self.ia_type, value="random").pack(pady=5)

        # Noms des joueurs
        self.names_frame = ctk.CTkFrame(self.window)
        self.names_frame.pack(pady=20, padx=20, fill="x")

        self.player1_name = ctk.CTkEntry(self.names_frame, placeholder_text="Nom du Joueur 1")
        self.player1_name.pack(pady=5)

        self.player2_name = ctk.CTkEntry(self.names_frame, placeholder_text="Nom du Joueur 2")
        self.player2_name.pack(pady=5)

        # Bouton de lancement
        self.start_button = ctk.CTkButton(self.window, text="Lancer la partie", command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        p1_name = self.player1_name.get() or "Joueur 1"
        p2_name = self.player2_name.get() or "Joueur 2"

        if self.mode.get() == "pvp":
            p1 = Human(p1_name)
            p2 = Human(p2_name)
        else:
            p1 = Human(p1_name)
            if self.ia_type.get() == "trained":
                p2 = ia_player(p2_name)
                p2.download()  # Charge l'IA entraînée
            else:
                p2 = Player(p2_name)  # IA aléatoire

        self.window.destroy()
        game = GameControler(p1, p2)
        game.start()


if __name__ == "__main__":
    config = GameConfig()
    config.window.mainloop()

