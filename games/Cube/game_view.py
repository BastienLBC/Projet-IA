import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GameView(ctk.CTk):
    def __init__(self, controller) -> None:
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
        cell_size = 50
        player1 = self.controller.model.players1
        player2 = self.controller.model.players2

        self.canvas.create_oval(
            player1.x * cell_size, player1.y * cell_size,
            (player1.x + 1) * cell_size, (player1.y + 1) * cell_size,
            fill=player1.color, outline="black"
        )
        self.canvas.create_oval(
            player2.x * cell_size, player2.y * cell_size,
            (player2.x + 1) * cell_size, (player2.y + 1) * cell_size,
            fill=player2.color, outline="black"
        )

    def update_view(self) -> None:
        self.draw_board()
        self.message_label.configure(text=self.controller.get_status_message())

    def reset(self):
        self.update_view()

    def end_game(self):
        self.message_label.configure(text="Fin du jeu !")