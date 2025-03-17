"""
Vue du jeu cubee
Règles : But :

Posséder plus de cases que l’adversaire

Déroulement :

Deux joueurs s'affrontent sur un plateau carré d'une taille variable (5x5 cases par défaut).

Un joueur gagne des cases en se déplaçant dessus.

Au début de la partie, les joueurs commencent chacun dans un coin opposé du terrain. Chacun à leur tour, ils vont se déplacer d'une case (vers le haut, le bas, la gauche ou la droite). Un joueur ne peut pas se déplacer sur une case appartenant au joueur adverse ni sortir des limites du plateau.
"""

import customtkinter as ctk

from game_controller import GameController

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GameView(ctk.CTk):
    def __init__(self,controller)->None:
        """
        initialisation de gameView
        Args:
            controller:
        """
        super().__init__()
        self.controller = controller
        self.title("Cubee")
        self.minsize(800, 500)
        self.maxsize(800, 500)

        self.message_label = ctk.CTkLabel(
            self,
            text="",
            font=("OCR A Extended",20, "bold"),
            text_color="#32CD32",
            padx = 30
        )
        self.message_label.pack(pady=20)

        self.canvas = ctk.CTkCanvas(self, width=725, height=325,bg= "#323232")
        self.canvas.pack()

        self.update_view()

    def draw_board(self)->None:
        """
        créateur du tableau en colorant les cases du plateau où les joueurs sont passés (dans la couleur du joueur(Un des joueurs a le vert et l'autre gris clair))
        """


    def update_view(self)->None:
        """
        Met à jour la vue et le tableau
        """


    def reset(self):
        pass

    def end_game(self):
        pass

