import customtkinter as ctk
import os
from games.pixelKart.pixelKart_dao import get_all
from games.pixelKart.pixelKart import main as pixelkart_main
import subprocess


selected_circuit = "Basic"

def launch_game(game):
    if game == "cube":
        os.system("python games/Cube/main.py")
    elif game == "alumettes":
        os.system("python games/torches/Alumettes.py")
    elif game == "pixelkart":
        if selected_circuit:
            subprocess.run(["python", "games/pixelKart/pixelKart.py", selected_circuit])
        else:
            print("Veuillez sélectionner un circuit avant de lancer le jeu.")

def update_selected_circuit(new_circuit):
    global selected_circuit
    selected_circuit = new_circuit



root = ctk.CTk()
root.title("Launcher")
root.minsize(800, 250)
root.maxsize(800, 250)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

frame_cube = ctk.CTkFrame(root, fg_color="#323232")
frame_alumettes = ctk.CTkFrame(root, fg_color="#323232")
frame_pixelkart = ctk.CTkFrame(root, fg_color="#323232")

frame_cube.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame_alumettes.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
frame_pixelkart.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

label_cube = ctk.CTkLabel(frame_cube, text="Cubee", font=("OCR A Extended", 20, "bold"), text_color="#32CD32")
label_cube.pack(pady=20)
button_cube = ctk.CTkButton(frame_cube, text="Jouer", command=lambda: launch_game("cube"))
button_cube.pack(pady=10)

label_alumettes = ctk.CTkLabel(frame_alumettes, text="Alumettes", font=("OCR A Extended", 20, "bold"), text_color="#32CD32")
label_alumettes.pack(pady=20)
button_alumettes = ctk.CTkButton(frame_alumettes, text="Jouer", command=lambda: launch_game("alumettes"))
button_alumettes.pack(pady=10)

label_pixelkart = ctk.CTkLabel(frame_pixelkart, text="PixelKart", font=("OCR A Extended", 20, "bold"), text_color="#32CD32")
label_pixelkart.pack(pady=20)
button_pixelkart = ctk.CTkButton(frame_pixelkart, text="Jouer", command=lambda: launch_game("pixelkart"))
button_pixelkart.pack(pady=10)

circuits = get_all()
circuit_names = list(circuits.keys())

circuit_var = ctk.StringVar(value=selected_circuit)
circuit_dropdown = ctk.CTkOptionMenu(frame_pixelkart, values=circuit_names, command=update_selected_circuit, variable=circuit_var)
circuit_dropdown.pack(pady=10)

root.mainloop()