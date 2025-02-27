from tkinter import *
class GameView(Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Jeu des allumettes")
        
        self.message_label = Label(self, text="", font=("Arial", 14))
        self.message_label.pack()
        
        self.canvas = Canvas(self, width=800, height=400)
        self.canvas.pack()
        
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack()
        
        self.buttons = []
        for i in range(1, 4):
            button = Button(self.buttons_frame, text=f"Prendre {i}", command=lambda n=i: self.controller.handle_human_move(n))
            button.pack(side="left")
            self.buttons.append(button)
        
        self.update_view()
    
    def update_view(self):
        self.canvas.delete("all")
        self.draw_matches(self.controller.get_nb_matches())
        self.message_label.config(text=self.controller.get_status_message())
    
    def draw_matches(self, count):
        for i in range(count):
            x = 20 + i * 30
            self.canvas.create_line(x, 50, x, 150, width=10, fill='brown')
            self.canvas.create_rectangle((x, 50), (x, 50), width=10, fill='orange')
            
    def end_game(self): 
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        reset_button = Button(self.buttons_frame, text="Recommencer", command=self.controller.reset_game)
        reset_button.pack()
    
    def reset(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        self.buttons = []
        for i in range(1, 4):
            button = Button(self.buttons_frame, text=f"Prendre {i}", command=lambda n=i: self.controller.handle_human_move(n))
            button.pack(side="left")
            self.buttons.append(button)
        self.update_view()
