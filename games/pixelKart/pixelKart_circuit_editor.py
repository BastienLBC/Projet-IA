import tkinter as tk
from tkinter import Tk, ttk
from games.pixelKart.pixelKart_dao import get_all, save_circuit
from games.pixelKart.pixelKart_circuitFrames import CircuitEditorFrame
class CircuitEditor(tk.Toplevel):
    """
    CircuitEditor is a graphical user interface (GUI) application for creating and editing circuit grids.
    It inherits from Toplevel to be used as a secondary window.
    Attributes:
        length_var (tk.StringVar): A Tkinter variable to store the length of the grid.
        width_var (tk.StringVar): A Tkinter variable to store the width of the grid.
        all_circuits (dict): A dictionary containing all available circuits retrieved from the data access object (DAO).
        grid_frame (CircuitEditorFrame): A custom frame for displaying and interacting with the circuit grid.
        circuit_var (tk.StringVar): A Tkinter variable to store the name of the selected circuit for import.
        callback (function): A callback function to be executed when a circuit is chosen.
    Methods:
        __init__():
            Initializes the CircuitEditor GUI, setting up the layout, input fields, and grid frame.
        import_circuit():
            Updates the grid frame with the circuit's data.
        save_circuit():
            Ask a name and saves the circuit using the DAO.
        change_size():
            Updates the grid size based on the user-provided length and width values.
    """

    def __init__(self, parent, callback):
        """
        Initializes the CircuitEditor GUI. Requires a parent window.
        Precondition : 
            callback is a fonction which take one str argument
        """
        super().__init__(parent)
        self.title("Circuit Editor")

        self.callback = callback

        self.length_var = tk.StringVar(value="20")
        self.width_var = tk.StringVar(value="12")
        self.all_circuits = dao.get_all()

        # Input frame for name, length and width
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=5, fill="x")

        ttk.Label(input_frame, text="Length:").pack(side="left", padx=5)
        length_entry = ttk.Entry(input_frame, textvariable=self.length_var, width=5)
        length_entry.pack(side="left")

        ttk.Label(input_frame, text="Width:").pack(side="left", padx=5)
        width_entry = ttk.Entry(input_frame, textvariable=self.width_var, width=5)
        width_entry.pack(side="left")
        # Buttun to change size
        change_size_button = ttk.Button(input_frame, text="Change size", command=self.change_size)
        change_size_button.pack(side="left", padx=5)

        # Frame for grid
        self.grid_frame = CircuitEditorFrame(self)
        self.grid_frame.pack(pady=10, fill="both", expand=True)

        # Frame to import existing
        import_frame = ttk.Frame(self)
        import_frame.pack(pady=5, fill="x")

        circuit_label = tk.Label(import_frame, text="Import circuit:")
        circuit_label.pack(side="left", padx=5)
        self.circuit_var = tk.StringVar()
        self.circuit_dropdown = tk.OptionMenu(import_frame, self.circuit_var, *list(self.all_circuits.keys()))
        self.circuit_var.set(list(self.all_circuits.keys())[0] if self.all_circuits.keys() else "")
        self.circuit_dropdown.pack(side="left", padx=5)
        import_button = ttk.Button(import_frame, text="Import", command=self.import_circuit)
        import_button.pack(side="left", padx=5)

        # Frame to save
        save_frame = ttk.Frame(self)
        save_frame.pack(pady=5, fill="x")

        save_button = ttk.Button(save_frame, text="Save", command=self.save_circuit)
        save_button.pack(side="left", padx=5)

        chose_button = ttk.Button(save_frame, text="Chose", command=self.chose)
        chose_button.pack(side="left", padx=5)
    
    def chose(self):
        """
        Calls the callback function with the selected circuit name.
        This method is typically used to notify the parent window about the selected circuit.
        """
        circuit_name = self.circuit_var.get()
        self.callback(circuit_name)

    def import_circuit(self):
        """
        Imports a circuit based on the selected circuit name from the user interface.
        This method retrieves the circuit data transfer object (DTO) corresponding to the 
        selected circuit name and updates the grid frame with the circuit's data.
        If the circuit name does not exist in the available circuits, an error message is printed.
        """
        
        circuit_name = self.circuit_var.get()
        print(f"Import {circuit_name}")
        if circuit_name in self.all_circuits:
            dto = self.all_circuits[circuit_name]
            print(f"=> {dto}")
        else:
            print(f"Error: Circuit '{circuit_name}' not found.")
            return
        self.grid_frame.dto_to_grid(dto)
        
        self.length_var.set(self.grid_frame.cols)
        self.width_var.set(self.grid_frame.rows)

    def save_circuit(self):
        """
        Opens a popup to ask for the circuit name and saves the circuit using the DAO.
        """
        def save_action():
            circuit_name = name_var.get()
            circuit_data = self.grid_frame.grid_to_dto()
            try :
                dao.save_circuit(circuit_name, circuit_data)
                self.all_circuits[circuit_name] = circuit_data
                self.circuit_var.set(circuit_name)
                self.circuit_dropdown['menu'].add_command(label=circuit_name, command=tk._setit(self.circuit_var, circuit_name))
                popup.destroy()
            except Exception as e:
                error_popup = tk.Toplevel(self)
                error_popup.title("Error")
                ttk.Label(error_popup, text=f"An error occurred: {str(e)}").pack(pady=10)
                ttk.Button(error_popup, text="OK", command=error_popup.destroy).pack(pady=5)
                

        popup = tk.Toplevel(self)
        popup.title("Save Circuit")

        ttk.Label(popup, text="Circuit Name:").pack(pady=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(popup, textvariable=name_var)
        name_entry.pack(pady=5)

        save_popup_button = ttk.Button(popup, text="Save", command=save_action)
        save_popup_button.pack(pady=5)

    def change_size(self):
        """
        change the size based on length and width entry
        """
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

        def reload_circuits(self):
            """Recharge les circuits et met à jour la liste déroulante."""
            self.all_circuits = dao.get_all()
            menu = self.circuit_dropdown['menu']
            menu.delete(0, 'end')
            for circuit_name in self.all_circuits.keys():
                menu.add_command(label=circuit_name, command=tk._setit(self.circuit_var, circuit_name))

        def save_circuit(self):
            """
            Opens a popup to ask for the circuit name and saves the circuit using the DAO.
            """

            def save_action():
                circuit_name = name_var.get()
                circuit_data = self.grid_frame.grid_to_dto()
                try:
                    save_circuit(circuit_name, circuit_data)  # Utilise la fonction DAO pour sauvegarder
                    self.reload_circuits()  # Recharge la liste des circuits
                    self.circuit_var.set(circuit_name)
                    popup.destroy()
                except Exception as e:
                    error_popup = tk.Toplevel(self)
                    error_popup.title("Error")
                    ttk.Label(error_popup, text=f"An error occurred: {str(e)}").pack(pady=10)
                    ttk.Button(error_popup, text="OK", command=error_popup.destroy).pack(pady=5)

            popup = tk.Toplevel(self)
            popup.title("Save Circuit")

            ttk.Label(popup, text="Circuit Name:").pack(pady=5)
            name_var = tk.StringVar()
            name_entry = ttk.Entry(popup, textvariable=name_var)
            name_entry.pack(pady=5)

            save_popup_button = ttk.Button(popup, text="Save", command=save_action)
            save_popup_button.pack(pady=5)

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the root window
    editor = CircuitEditor(root, callback=lambda x : print(f"Callback with {x}"))
    editor.mainloop()