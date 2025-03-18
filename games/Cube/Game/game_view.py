import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GameView(ctk.CTk):
    def __init__(self, controller) -> None:
        """
        Initialisation de GameView
        Args:
            controller: Instance du contrôleur du jeu
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

        self.bind_all("<Key>", self.on_key_press)

        self.update_view()

        self.reset_button = ctk.CTkButton(self, text="Recommencer", command=self.controller.reset_game)
        self.reset_button.pack_forget()

    def on_key_press(self, event):
        """
        Récupère la touche pressée au clavier et appelle la fonction de déplacement du contrôleur
        """
        touche = event.keysym.upper()
        self.controller.handle_player_moove(touche)

    def draw_board(self) -> None:
        """
        Dessine le plateau en colorant les cases selon les joueurs
        """
        self.canvas.delete("all")
        board = self.controller.model.matrix
        cell_size = 50
        board_width = len(board) * cell_size
        board_height = len(board[0]) * cell_size

        offset_x = (725 - board_width) // 2
        offset_y = (325 - board_height) // 2

        for x in range(len(board)):
            for y in range(len(board[x])):
                color = board[x][y]["color"]
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
        """
        Réinitialise la vue
        """
        self.update_view()
        self.reset_button.pack_forget()

    def end_game(self):
        """
        Affiche le message de fin de jeu et recommencer
        """
        self.message_label.configure(text="Fin du jeu !")
        self.reset_button.pack(pady=10)