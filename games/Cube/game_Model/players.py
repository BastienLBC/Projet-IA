class Player:

    def __init__(self,name:str, color:str)-> None:
        self.name = name
        self.color = color

        self.x = 0
        self.y = 0

        self.score = 1

class Random(Player):
    def __init__(self)->None:
        super().__init__("Random", "grey")