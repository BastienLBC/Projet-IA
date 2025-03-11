import customtkinter as ctk
from tkinter import messagebox
import torches.Alumettes as Alumettes

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Projet IA")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both")

        self.create_main_menu()

    def create_main_menu(self):
        title_label = ctk.CTkLabel(self.main_frame, text="Projet IA", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)

        game_frame = ctk.CTkFrame(self.main_frame)
        game_frame.pack(pady=20)

        ctk.CTkButton(game_frame, text="Jouer - Allumettes", command=self.launch_allumettes,
                      width=200, height=40).pack(pady=10)
        ctk.CTkButton(game_frame, text="Jouer - Cubee", command=self.placeholder,
                      width=200, height=40).pack(pady=10)
        ctk.CTkButton(game_frame, text="Jouer - PixelKart", command=self.placeholder,
                      width=200, height=40).pack(pady=10)

    def launch_allumettes(self):
        Alumettes.start()
        
    def placeholder(self):
        messagebox.showinfo("pas créé", "Il faudra patienter")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()