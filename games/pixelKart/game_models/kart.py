import random
from games.pixelKart.const import PIXEL_TYPES
from games.pixelKart.dao import find_entry_by_key, save_entry

class kart:
    
    def __init__(self,name:str):

        self.name = name
        self.x = 0
        self.y = 0 
        self.direction = "Est"
        self.speed = 0
        self.laps = 0
        self.inLife = True

        self.wins = 0
        self.losses = 0

    #@staticmethod
    def play(self):
        """
        Retourne une direction reçu par l'utilisateur
        """
        #commence en direction EST
        return random.choice(['Accelerate', 'Decelerate', 'Left', 'Right', 'Nothing'])
    
    def win(self) -> None:
        """
        Ajoute une victoire au nb de victoires
        """
        self.wins += 1

    def lose(self) -> None:
        """
        Ajoute une défaite au nb de défaites
        """
        self.losses += 1

class humanKart(kart):
    def __init__(self, name:str):
        super().__init__(name)
        
    def play(self):
        """
        Retourne un bind reçu par l'utilisateur
        """
        return self.Event

class aiKart(kart):
    
    def __init__(self, name: str, learning_rate: float = 0.01, gamma: float = 0.9,
                 epsilon: float = 0.9) -> None:
        super().__init__(name)
        self.lr = learning_rate
        self.gamma = gamma
        self.eps = epsilon
        self.board = None
        self.q_table = {}

    def get_q_value(self, key):
        entry = find_entry_by_key(key)
        q_value = entry['reward'] if entry else 0.0
        print(f"Loaded Q-value for {key}: {q_value}")
        return q_value

    def set_q_value(self, key, reward):
        save_entry({'unique_key': key, 'reward': reward})

    def type_case(self,xi,yi):
        case_type = None
        if self.circuit:
            x, y = xi, yi
            if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]):
                case_letter = self.grid[y][x]
                case_type = next(
                    (case for case, properties in PIXEL_TYPES.items() if properties["letter"] == case_letter),
                    None)
        return case_type

        
        
