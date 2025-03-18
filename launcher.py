import customtkinter as ctk
import os

def launch_game(game):
    if game == "cube":
        os.system("python games/Cube/main.py")
    elif game == "alumettes":
        os.system("python games/torches/Alumettes.py")

root = ctk.CTk()
root.title("Launcher")
root.minsize(800, 250)
root.maxsize(800, 250)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

frame_cube = ctk.CTkFrame(root, fg_color="#323232")
frame_alumettes = ctk.CTkFrame(root, fg_color="#323232")

frame_cube.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame_alumettes.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

label_cube = ctk.CTkLabel(frame_cube, text="Cube", font=("OCR A Extended", 20, "bold"), text_color="#32CD32")
label_cube.pack(pady=20)
button_cube = ctk.CTkButton(frame_cube, text="Jouer", command=lambda: launch_game("cube"))
button_cube.pack(pady=10)
label_alumettes = ctk.CTkLabel(frame_alumettes, text="Alumettes", font=("OCR A Extended", 20, "bold"), text_color="#32CD32")
label_alumettes.pack(pady=20)
button_alumettes = ctk.CTkButton(frame_alumettes, text="Jouer", command=lambda: launch_game("alumettes"))
button_alumettes.pack(pady=10)

root.mainloop()