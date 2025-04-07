import tkinter as tk
from tkinter import ttk
import const

class CircuitFrame(ttk.Frame):
    """
    CircuitFrame is a custom ttk.Frame widget that represents a grid-based circuit. 
    The class provides functionality to initialize the grid, clear it,,
    and serialize/deserialize the grid state for saving and loading purposes.
    Attributes:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        cells (list): A 2D list of tkinter Label widgets representing the grid cells.
    Methods:
        draw():
            draw cells.
        init_cells():
            Initialize the grid with road and grass on the borders.
        clear():
            Clears the grid by destroying all cell widgets and resetting the cells list.
        grid_to_dto():
            Serializes the grid into a string representation, where each cell is represented 
            by a letter corresponding to its terrain type.
        dto_to_grid(dto):
            Deserializes a string representation of the grid and updates the grid display 
            and cells list accordingly.
    """
    def __init__(self,container, circuit=None, rows=12, cols=20):
        """
        Initialize the CircuitFrame with a specified number of rows and columns.
        Args:
            container (tkinter.Tk): The parent widget/container.
            circuit (Circuit): Optional DTO_Circuit object to initialize the grid with.
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
        """
        super().__init__(container)
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.init_cells()
        if circuit:
            self.dto_to_grid(circuit)

    def init_cells(self):
        """
        Initialize the grid with road and grass on the borders.
        update the display and the cells list.
        """        
        for line in range(self.rows):
            row = []
            for col in range(self.cols):
                initial_type = "GRASS" if 0 in (line,col) or line == self.rows - 1 or col == self.cols - 1 else "ROAD"
                initial_color = const.PIXEL_TYPES[initial_type]["color"]
                cell = tk.Label(self, bg=initial_color, width=2, height=1, borderwidth=1, relief="solid")
                cell.grid(row=line, column=col, sticky="nsew")
                
                row.append(cell)
            self.cells.append(row)

        for i in range(self.rows):
            self.grid_rowconfigure(i, weight=1, minsize=20)
        for j in range(self.cols):
            self.grid_columnconfigure(j, weight=1, minsize=20)

    def clear(self):
        """
        Clear the grid.
        """
        for widget in self.winfo_children():
            widget.destroy()

        self.cells.clear() 
    
    
    def grid_to_dto(self):
        """
        Return the grid as a string look like "rgc,rgc,rgc".
        """
        export_result = []
        color_map = dict((v["color"], v["letter"]) for v in const.PIXEL_TYPES.values())
        for row in self.cells:
            export_result.append("".join(color_map[cell.cget("bg")] for cell in row))
        return ",".join(export_result)

    def dto_to_grid(self, dto):
        """
        Args : dto (str) look like "rgc,rgc,rgc" 
        """
        import_data = dto.split(",")
        if not import_data:
            return
        
        self.rows = len(import_data)
        self.cols = len(import_data[0])

        self.clear()
        self.init_cells()

        color_map = dict((v["letter"], v["color"]) for v in const.PIXEL_TYPES.values())
        for i, row in enumerate(import_data):
            for j, char in enumerate(row):
                if i < len(self.cells) and j < len(self.cells[i]):
                    cell = self.cells[i][j]
                    cell.config(bg=color_map.get(char, "grey"))


class CircuitEditorFrame (CircuitFrame):
    """
    CircuitEditorFrame is a custom ttk.Frame widget that represents a circuit editor.
    It allows users to create and manipulate a grid-based circuit, where each cell can represent different types of terrain (e.g., road, grass).
    The class provides functionality to initialize the grid, clear it, change cell colors,
    and serialize/deserialize the grid state for saving and loading purposes.

    Methods :
        init_cells():
            Initializes the grid with default terrain types (road and grass) and updates 
            the display and cells list. Add a listener on Labels.
        change_color(x, y):
            Changes the color of the cell at position (x, y) in a cyclic order based on 
            the defined PIXEL_TYPES.
    """

    def init_cells(self):
        """
        Add a listener on Labels.
        """
        super().init_cells()
        for line in range(self.rows):
                for col in range(self.cols):
                    cell = self.cells[line][col]
                    cell.bind("<Button-1>", lambda e, x=line, y=col: self.change_color(x, y))
        
    def change_color(self, x, y):
        """
        change the color of the cell at position x, y.
        Color change in order of PIXEL_TYPES.
        """
        current_color = self.cells[x][y].cget("bg")
        colors = [pixel["color"] for pixel in const.PIXEL_TYPES.values()]
        new_color = colors[(colors.index(current_color) + 1) % len(colors)]
        self.cells[x][y].config(bg=new_color)

class CircuitRaceFrame (CircuitFrame):
    """
    CircuitRaceFrame is a subclass of CircuitFrame that represents a race circuit frame 
    with the ability to display karts on the circuit grid.
    Attributes:
        karts_cells (list): A list to store the tkinter Label widgets representing the karts.
    Methods:
        __init__(container, circuit=None, rows=12, cols=20):
            Initializes the CircuitRaceFrame with the given container, circuit, 
            number of rows, and columns. karts are sets to [].
        update_view(karts):
            Updates the view of the circuit by clearing the previous kart cells and 
            adding new kart cells based on the provided karts dictionary.
    """
    def __init__(self, container, circuit=None, rows=12, cols=20):
        super().__init__(container, circuit, rows, cols)
        self.karts_cells = []

    def update_view(self, karts):
        """
        Args : 
            kart : dict : {position: color}
        """
        # Clear previous kart cells
        for cell in self.karts_cells:
            cell.destroy()
        self.karts_cells.clear()

        # Add new kart cells
        for position, color in karts.items():
            line, col = position
            if 0 <= line < self.rows and 0 <= col < self.cols:
                cell = tk.Label(self, bg=color, width=2, height=1, borderwidth=1, relief="solid")
                cell.grid(row=line, column=col, sticky="nsew")
                self.karts_cells.append(cell)

        

        