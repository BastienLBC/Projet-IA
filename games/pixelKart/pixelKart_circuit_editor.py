# python
import customtkinter as ctk
from games.pixelKart.pixelKart_dao import get_all, save_circuit as dao_save_circuit, update_circuit
from games.pixelKart.pixelKart_circuitFrames import CircuitEditorFrame

class CircuitEditor(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Circuit Editor")
        self.geometry("800x600")
        self.length_var = ctk.StringVar(value="20")
        self.width_var = ctk.StringVar(value="12")
        self.all_circuits = get_all()

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Zone de saisie pour la taille
        size_frame = ctk.CTkFrame(main_frame)
        size_frame.pack(pady=(10,5), fill="x")
        ctk.CTkLabel(size_frame, text="Length:").pack(side="left", padx=5)
        length_entry = ctk.CTkEntry(size_frame, textvariable=self.length_var, width=60)
        length_entry.pack(side="left", padx=5)
        ctk.CTkLabel(size_frame, text="Width:").pack(side="left", padx=5)
        width_entry = ctk.CTkEntry(size_frame, textvariable=self.width_var, width=60)
        width_entry.pack(side="left", padx=5)
        change_size_button = ctk.CTkButton(size_frame, text="Change size", command=self.change_size)
        change_size_button.pack(side="left", padx=5)

        # Zone de saisie pour le nom du circuit
        name_frame = ctk.CTkFrame(main_frame)
        name_frame.pack(pady=(5,10), fill="x")
        ctk.CTkLabel(name_frame, text="Nom du circuit:").pack(side="left", padx=5)
        self.name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(name_frame, textvariable=self.name_var)
        name_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Cadre de la grille
        self.grid_frame = CircuitEditorFrame(main_frame)
        self.grid_frame.init_cells()
        self.grid_frame.pack(pady=10, fill="both", expand=True)

        # Cadre des actions
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(pady=(10,5), fill="x")
        # Import existant
        import_frame = ctk.CTkFrame(action_frame)
        import_frame.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(import_frame, text="Import circuit:").pack(side="left", padx=5)
        self.circuit_var = ctk.StringVar()
        circuit_options = list(self.all_circuits.keys())
        self.circuit_dropdown = ctk.CTkOptionMenu(import_frame, values=circuit_options, variable=self.circuit_var)
        if circuit_options:
            self.circuit_var.set(circuit_options[0])
        self.circuit_dropdown.pack(side="left", padx=5)
        import_button = ctk.CTkButton(import_frame, text="Import", command=self.import_circuit)
        import_button.pack(side="left", padx=5)
        # Actions Save et Chose
        act_buttons = ctk.CTkFrame(action_frame)
        act_buttons.pack(side="right", fill="x", expand=True, padx=5)
        save_button = ctk.CTkButton(act_buttons, text="Save", command=self.save_circuit)
        save_button.pack(side="left", padx=5)
        chose_button = ctk.CTkButton(act_buttons, text="Chose", command=self.chose)
        chose_button.pack(side="left", padx=5)

    def chose(self):
        circuit_name = self.circuit_var.get()
        self.callback(circuit_name)
        self.destroy()

    def import_circuit(self):
        circuit_name = self.circuit_var.get()
        if circuit_name in self.all_circuits:
            dto = self.all_circuits[circuit_name]
        else:
            self.show_popup("Erreur", f"Circuit '{circuit_name}' introuvable.")
            return
        self.grid_frame.dto_to_grid(dto)
        self.length_var.set(self.grid_frame.cols)
        self.width_var.set(self.grid_frame.rows)

    def save_circuit(self):
        circuit_name = self.name_var.get().strip()
        if not circuit_name:
            self.show_popup("Erreur", "Veuillez renseigner un nom pour le circuit.")
            return
        circuit_data = self.grid_frame.grid_to_dto()
        try:
            circuits = get_all()
            if circuit_name in circuits:
                if not self.ask_yes_no("Confirmation", "Ce circuit existe déjà. Voulez-vous le remplacer ?"):
                    return
                update_circuit(circuit_name, circuit_data)
            else:
                dao_save_circuit(circuit_name, circuit_data)
            self.all_circuits[circuit_name] = circuit_data
            self.circuit_var.set(circuit_name)
            self.circuit_dropdown.configure(values=list(self.all_circuits.keys()))
            self.show_popup("Succès", "Le circuit a été sauvegardé avec succès.")
        except Exception as e:
            self.show_popup("Erreur", f"Erreur lors de la sauvegarde : {str(e)}")

    def change_size(self):
        try:
            rows = int(self.width_var.get())
        except ValueError:
            rows = 12
            self.width_var.set(str(rows))
        try:
            cols = int(self.length_var.get())
        except ValueError:
            cols = 20
            self.length_var.set(str(cols))
        self.grid_frame.rows = rows
        self.grid_frame.cols = cols
        self.grid_frame.clear()
        self.grid_frame.init_cells()

    def show_popup(self, title, message):
        popup = ctk.CTkToplevel(self)
        popup.grab_set()
        popup.title(title)
        popup.geometry("300x150")
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14))
        label.pack(pady=20, padx=10)
        ok_button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)
        popup.wait_window()

    def ask_yes_no(self, title, message):
        result = [None]
        popup = ctk.CTkToplevel(self)
        popup.grab_set()
        popup.title(title)
        popup.geometry("300x150")
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14))
        label.pack(pady=20, padx=10)
        def yes():
            result[0] = True
            popup.destroy()
        def no():
            result[0] = False
            popup.destroy()
        button_frame = ctk.CTkFrame(popup)
        button_frame.pack(pady=10)
        yes_button = ctk.CTkButton(button_frame, text="Oui", command=yes)
        yes_button.pack(side="left", padx=5)
        no_button = ctk.CTkButton(button_frame, text="Non", command=no)
        no_button.pack(side="left", padx=5)
        popup.wait_window()
        return result[0]