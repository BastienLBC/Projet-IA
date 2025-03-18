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
        (dans la couleur du joueur)
        """
        self.canvas.delete("all")
        board = self.controller.model.matrix
        cell_size = 50
        board_width = len(board) * cell_size  # Largeur totale du plateau
        board_height = len(board[0]) * cell_size  # Hauteur totale du plateau

        # Calcul des offsets pour centrer le plateau dans le canvas
        offset_x = (725 - board_width) // 2  # 725 = largeur du canvas
        offset_y = (325 - board_height) // 2  # 325 = hauteur du canvas

        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] is None:
                    color = "white"
                else:
                    color = board[x][y].color
                self.canvas.create_rectangle(
                    offset_x + x * cell_size, offset_y + y * cell_size,
                    offset_x + (x + 1) * cell_size, offset_y + (y + 1) * cell_size,
                    fill=color, outline="black"
                )
        self.draw_players(offset_x, offset_y)

    def draw_players(self, offset_x, offset_y) -> None:
        """
        Dessine les joueurs sur le plateau avec un décalage pour le centrage
        """
        cell_size = 50
        player1 = self.controller.model.players1
        player2 = self.controller.model.players2

        self.canvas.create_oval(
            offset_x + player1.x * cell_size, offset_y + player1.y * cell_size,
            offset_x + (player1.x + 1) * cell_size, offset_y + (player1.y + 1) * cell_size,
            fill=player1.color
        )
        self.canvas.create_oval(
            offset_x + player2.x * cell_size, offset_y + player2.y * cell_size,
            offset_x + (player2.x + 1) * cell_size, offset_y + (player2.y + 1) * cell_size,
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