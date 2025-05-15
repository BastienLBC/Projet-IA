import customtkinter as ctk
from games.pixelKart.pixelKart_dao import get_all
from games.pixelKart.pixelKart_circuit_editor import CircuitEditor
import subprocess

class PixelKartSettings(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Paramètres PixelKart")
        self.geometry("600x800")
        self.circuit_var = ctk.StringVar(value="")
        self.laps_var = ctk.IntVar(value=5)
        self.player_mode_var = ctk.StringVar(value="Humain vs Random")
        self.circuits = get_all()

        ctk.CTkLabel(self, text="Choisir un circuit :").pack(pady=10)
        self.circuit_dropdown = ctk.CTkOptionMenu(self, values=list(self.circuits.keys()), variable=self.circuit_var)
        self.circuit_dropdown.pack(pady=10)

        ctk.CTkLabel(self, text="Nombre de tours :").pack(pady=10)
        laps_entry = ctk.CTkEntry(self, textvariable=self.laps_var)
        laps_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Mode de jeu :").pack(pady=10)
        self.player_mode_dropdown = ctk.CTkOptionMenu(self, values=["Humain vs Random", "Humain vs IA"], variable=self.player_mode_var)
        self.player_mode_dropdown.pack(pady=10)

        ctk.CTkButton(self, text="Ouvrir l'éditeur de circuits", command=self.open_circuit_editor).pack(pady=10)
        ctk.CTkButton(self, text="Sauvegarder et fermer", command=self.save_and_close).pack(pady=20)


    def open_circuit_editor(self):
        editor = CircuitEditor(self, callback=lambda x: self.circuit_var.set(x))
        editor.grab_set()

    def import_circuit(self):
        pass

    def export_circuit(self):
        pass

    def save_and_close(self):
        global selected_circuit, selected_laps, selected_mode
        selected_circuit = self.circuit_var.get()
        try:
            selected_laps = int(self.laps_var.get())
            if selected_laps <= 0:
                raise ValueError("Le nombre de tours doit être supérieur à 0.")
        except ValueError:
            selected_laps = None

        selected_mode = self.player_mode_var.get()

        if not selected_circuit or selected_laps is None or not selected_mode:
            popup = ctk.CTkToplevel(self)
            popup.title("Erreur")
            popup.geometry("300x150")
            ctk.CTkLabel(popup, text="Veuillez remplir tous les champs correctement avant de sauvegarder.",
                         font=("Arial", 14), text_color="red").pack(pady=20)
            ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=10)
            return

        print(f"Paramètres sauvegardés : Circuit={selected_circuit}, Tours={selected_laps}, Mode={selected_mode}")
        self.callback(selected_circuit,selected_laps)
        self.destroy()