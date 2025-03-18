# """
# Vue du jeu cubee
# Règles : But :
#
# Posséder plus de cases que l’adversaire
#
# Déroulement :
#
# Deux joueurs s'affrontent sur un plateau carré d'une taille variable (5x5 cases par défaut).
#
# Un joueur gagne des cases en se déplaçant dessus.
#
# Au début de la partie, les joueurs commencent chacun dans un coin opposé du terrain. Chacun à leur tour, ils vont se déplacer d'une case (vers le haut, le bas, la gauche ou la droite). Un joueur ne peut pas se déplacer sur une case appartenant au joueur adverse ni sortir des limites du plateau.
# """
#
# import customtkinter as ctk
#
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("green")
#
# class GameView(ctk.CTk):
#     def __init__(self,controller)->None:
#         """
#         initialisation de gameView
#         Args:
#             controller:
#         """
#         super().__init__()
#         self.controller = controller
#         self.title("Cubee")
#         self.minsize(800, 500)
#         self.maxsize(800, 500)
#
#         self.message_label = ctk.CTkLabel(
#             self,
#             text="",
#             font=("OCR A Extended",20, "bold"),
#             text_color="#32CD32",
#             padx = 30
#         )
#         self.message_label.pack(pady=20)
#
#         self.canvas = ctk.CTkCanvas(self, width=725, height=325,bg= "#323232")
#         self.canvas.pack()
#
#         self.update_view()
#
#     def draw_board(self)->None:
#         """
#         créateur du tableau en colorant les cases du plateau où les joueurs sont passés (dans la couleur du joueur(Un des joueurs a le vert et l'autre gris clair))
#         """
#
#
#     def update_view(self)->None:
#         """
#         Met à jour la vue et le tableau
#         """
#
#
#     def reset(self):
#         pass
#
#     def end_game(self):
#         pass
#

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GameView(ctk.CTk):
    def __init__(self, controller) -> None:
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
            font=("OCR A Extended", 20, "bold"),
            text_color="#32CD32",
            padx=30
        )
        self.message_label.pack(pady=20)

        self.canvas = ctk.CTkCanvas(self, width=725, height=325, bg="#323232")
        self.canvas.pack()

        self.update_view()

    def draw_board(self) -> None:
        """
        Créateur du tableau en colorant les cases du plateau où les joueurs sont passés
        (dans la couleur du joueur (Un des joueurs a le vert et l'autre gris clair))
        """
        self.canvas.delete("all")
        board = self.controller.model.board
        cell_size = 50
        for x in range(len(board)):
            for y in range(len(board[x])):
                color = "white" if board[x][y] == "white" else board[x][y].color
                self.canvas.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color, outline="black"
                )
        self.draw_players()

    def draw_players(self) -> None:
        """
        Dessine les joueurs sur le plateau
        """
        cell_size = 50
        player1 = self.controller.model.players1
        player2 = self.controller.model.players2

        self.canvas.create_oval(
            player1.x * cell_size, player1.y * cell_size,
            (player1.x + 1) * cell_size, (player1.y + 1) * cell_size,
            fill=player1.color
        )
        self.canvas.create_oval(
            player2.x * cell_size, player2.y * cell_size,
            (player2.x + 1) * cell_size, (player2.y + 1) * cell_size,
            fill=player2.color
        )

    def update_view(self) -> None:
        """
        Met à jour la vue et le tableau
        """
        self.draw_board()
        self.message_label.configure(text=self.controller.get_status_message())

    def reset(self):
        self.update_view()

    def end_game(self):
        self.message_label.configure(text="Fin du jeu !")