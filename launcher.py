import customtkinter as ctk
import os
from games.pixelKart.pixelKart_dao import get_all
from games.pixelKart.pixelKart import main as pixelkart_main
import subprocess
from games.pixelKart.pixel_kart_settings import PixelKartSettings

selected_circuit = None
selected_laps = 2
selected_mode = "Humain vs Random"

def launch_game(game):
    if game == "cube":
        os.system("python games/Cube/main.py")
    elif game == "alumettes":
        os.system("python games/torches/Alumettes.py")
    elif game == "pixelkart":
        print(f"selected_circuit: {selected_circuit}, selected_laps: {selected_laps}, selected_mode: {selected_mode}")
        if selected_circuit and selected_laps and selected_mode:
            subprocess.run(["python", "games/pixelKart/pixelKart.py", selected_circuit, str(selected_laps), selected_mode])
        else:
            popup = ctk.CTkToplevel()
            popup.title("Erreur")
            popup.geometry("450x150")
            ctk.CTkLabel(popup, text="Veuillez sélectionner un circuit\net un nombre de tours avant de lancer le jeu.",
                         font=("Arial", 16, "underline"), text_color="lightgreen").pack(pady=20)
            ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=10)

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

label_cube = ctk.CTkLabel(frame_cube, text="Cube", font=("OCR A Extended", 20, "bold"), text_color="#32CD32")
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

button_pixelkart_settings = ctk.CTkButton(
    frame_pixelkart,
    text="Paramètres",
    command=lambda: PixelKartSettings(root, callback=update_selected)
)
button_pixelkart_settings.pack(pady=10)

def update_selected(new_circuit, new_laps):
    global selected_circuit, selected_laps
    selected_circuit = new_circuit
    selected_laps = new_laps
    print(f"Circuit sélectionné : {selected_circuit}, {selected_laps}")


root.mainloop()