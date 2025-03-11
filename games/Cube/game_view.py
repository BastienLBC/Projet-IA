import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GameView(ctk.CTk):
    def __init__(self, controller)->None:
        """
        initialisation de gameView
        Args:
            controller; instance de GameController
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

    def update_view(self)->None:
        """
        Met à jour l'écran en supprimant et remettant le nouveau tableau
        """
        pass
