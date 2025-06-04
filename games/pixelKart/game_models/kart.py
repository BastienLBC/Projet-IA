import random
from games.pixelKart.const import PIXEL_TYPES
from games.pixelKart.dao import find_entry_by_key, save_entry
from games.pixelKart.dico import generate_key

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
    
    def __init__(
        self,
        name: str,
        learning_rate: float = 0.01,
        gamma: float = 0.9,
        epsilon: float = 0.9,
    ) -> None:
        super().__init__(name)
        self.lr = learning_rate
        self.gamma = gamma
        self.eps = epsilon

        from games.pixelKart.dao import find_all_entries

        self.q_table = {
            entry["unique_key"]: entry["reward"] for entry in find_all_entries()
        }
        self.commit_frequency = 50
        self._pending = 0
        self.circuit = None
        self.grid = None

    def get_q_value(self, key):
        if key in self.q_table:
            return self.q_table[key]

        entry = find_entry_by_key(key)
        q_value = entry['reward'] if entry else 0.0
        self.q_table[key] = q_value
        print(f"Loaded Q-value for {key}: {q_value}")
        return q_value

    def set_q_value(self, key, reward):
        self.q_table[key] = reward
        save_entry({'unique_key': key, 'reward': reward}, commit=False)
        self._pending += 1
        if self._pending >= self.commit_frequency:
            from games.pixelKart.dao import commit_session

            commit_session()
            self._pending = 0

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

    # --- Q-learning helpers -------------------------------------------------

    def state_key(self):
        """Compute the state representation for the current position."""
        return generate_key(self.x, self.y, self.speed, self.type_case)

    def choose_action(self):
        actions = ["Accelerate", "Decelerate", "Left", "Right", "Nothing"]

        if random.random() < self.eps:
            return random.choice(actions)

        state = self.state_key()
        best_action = None
        best_value = float("-inf")
        for act in actions:
            key = f"{state}:{act}"
            value = self.get_q_value(key)
            if value > best_value:
                best_value = value
                best_action = act
        return best_action if best_action is not None else random.choice(actions)

    def update_q_table(self, state, action, reward, next_state):
        current_key = f"{state}:{action}"
        next_values = [self.get_q_value(f"{next_state}:{a}") for a in ["Accelerate", "Decelerate", "Left", "Right", "Nothing"]]
        next_q = max(next_values)
        current_q = self.get_q_value(current_key)
        new_q = current_q + self.lr * (reward + self.gamma * next_q - current_q)
        self.set_q_value(current_key, new_q)

    def next_epsilon(self, coef: float = 0.95, min_val: float = 0.05) -> None:
        self.eps *= coef
        if self.eps < min_val:
            self.eps = min_val

        
        
