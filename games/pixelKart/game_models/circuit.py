from games.pixelKart.const import PIXEL_TYPES
import random

class Circuit:
    def __init__(self, player1, player2, gp: str = None):
        self.player1 = player1
        self.player2 = player2
        self.start_line = []
        self.nb_laps = 2
        self.circuit = gp
        self.grid = [list(row) for row in gp.split(",")] if gp else None
        self.rows = 30
        self.cols = 30

        self.current_player = player1
        self.game_over = False

    def switch_player(self) -> None:
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def get_current_player(self) -> str:
        return self.current_player

    def moove(self):
        x = self.current_player.x
        y = self.current_player.y
        direction = self.current_player.direction
        speed = self.current_player.speed

        new_x, new_y = x, y
        if direction == 'Nord':
            new_y -= speed
        elif direction == 'Sud':
            new_y += speed
        elif direction == 'Ouest':
            new_x -= speed
        elif direction == 'Est':
            new_x += speed

        if not self.can_move(new_x, new_y):
            self.current_player.inLife = False
            self.current_player.speed = 0
            return

        if speed == 2:
            if (direction == 'Nord') and self.can_move(x, y - 1):
                self.speed_limiter()
                self.move_up(1)
                speed = 1
                if self.type_case() == "GRASS":
                    self.current_player.speed = 1
                    return
            elif (direction == 'Sud') and self.can_move(x, y + 1):
                self.speed_limiter()
                self.move_down(1)
                speed = 1
                if self.type_case() == "GRASS":
                    self.current_player.speed = 1
                    return
            elif (direction == 'Ouest') and self.can_move(x - 1, y):
                self.speed_limiter()
                self.move_left(1)
                speed = 1
                if self.type_case() == "GRASS":
                    self.current_player.speed = 1
                    return
            elif (direction == 'Est') and self.can_move(x + 1, y):
                self.speed_limiter()
                self.move_right(1)
                speed = 1
                self.cpt_laps()
                if self.type_case() == "GRASS":
                    self.current_player.speed = 1
                    return

        if speed in (1, -1):
            if (direction == 'Nord') and (self.can_move(x, y - 1) or self.can_move(x, y + 1)):
                self.speed_limiter()
                self.move_up(speed)
            elif (direction == 'Sud') and (self.can_move(x, y + 1) or self.can_move(x, y - 1)):
                self.speed_limiter()
                self.move_down(speed)
            elif (direction == 'Ouest') and (self.can_move(x - 1, y) and self.can_move(x + 1, y)):
                self.speed_limiter()
                self.move_left(speed)
            elif (direction == 'Est') and (self.can_move(x + 1, y) and self.can_move(x - 1, y)):
                self.speed_limiter()
                self.move_right(speed)
                self.cpt_laps()
            else:
                self.current_player.speed = 0

    def move_up(self, speed: int):
        self.current_player.y -= speed

    def move_down(self, speed: int):
        self.current_player.y += speed

    def move_left(self, speed: int):
        self.current_player.x -= speed

    def move_right(self, speed: int):
        self.current_player.x += speed

    def can_move(self, x, y):
        if self.grid:
            return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y])
        return 0 <= x < self.rows and 0 <= y < self.cols

    def speed_limiter(self):
        case_type = self.type_case()
        if case_type == "GRASS":
            self.current_player.speed = max(1, self.current_player.speed // 2)
        elif case_type == "WALL":
            self.current_player.inLife = False
            self.current_player.speed = 0
        elif case_type == "FINISH" and self.current_player.direction != "Est":
            self.current_player.inLife = False

    def type_case(self):
        case_type = None
        if self.circuit:
            x, y = self.current_player.x, self.current_player.y
            if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]):
                case_letter = self.grid[y][x]
                case_type = next(
                    (case for case, properties in PIXEL_TYPES.items() if properties["letter"] == case_letter),
                    None)
        return case_type

    def accelerate(self):
        if self.current_player.speed < 2:
            self.current_player.speed += 1

    def decelerate(self):
        if self.current_player.speed > -1:
            self.current_player.speed -= 1

    def turn_left(self):
        direction = self.current_player.direction
        if direction == "Nord":
            self.current_player.direction = "Ouest"
        elif direction == "Est":
            self.current_player.direction = "Nord"
        elif direction == "Sud":
            self.current_player.direction = "Est"
        else:
            self.current_player.direction = "Sud"

    def reset_game(self):
        self.game_over = False
        self.current_player = None
        self.player1.laps = 0
        self.player2.laps = 0
        self.player1.speed = 0
        self.player2.speed = 0
        self.player1.inLife = True
        self.player2.inLife = True
        self.player1.direction = "Est"
        self.player2.direction = "Est"
        self.load_start_line()
        self.start()

    def turn_right(self):
        direction = self.current_player.direction
        if direction == "Nord":
            self.current_player.direction = "Est"
        elif direction == "Est":
            self.current_player.direction = "Sud"
        elif direction == "Sud":
            self.current_player.direction = "Ouest"
        else:
            self.current_player.direction = "Nord"

    def one_action(self, bind):
        if self.game_over:
            return
        if self.current_player.inLife is False:
            return None

        if bind == "Accelerate":
            self.accelerate()
        elif bind == "Decelerate":
            self.decelerate()
        elif bind == "Left":
            self.turn_left()
        elif bind == "Right":
            self.turn_right()
        elif bind == "Nothing":
            return None

        self.moove()
        self.speed_limiter()
        # Vérifie si un joueur a terminé tous les tours
        if self.player1.laps >= self.nb_laps or self.player2.laps >= self.nb_laps:
            self.game_over = True

    def load_start_line(self):
        grid = [list(row) for row in self.circuit.split(',')]
        self.start_line = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == PIXEL_TYPES["FINISH"]["letter"]:
                    self.start_line.append((x, y))

    def start(self):
        self.load_start_line()
        if not self.start_line:
            raise ValueError("La ligne de départ est vide. Vérifiez que le circuit contient des cases 'F'.")
        pos1_index = random.randint(0, len(self.start_line) - 1)
        x1, y1 = self.start_line[pos1_index]
        self.player1.x = x1
        self.player1.y = y1

        pos2_index = random.randint(0, len(self.start_line) - 1)
        x2, y2 = self.start_line[pos2_index]
        self.player2.x = x2
        self.player2.y = y2

        self.current_player = self.player1

    def cpt_laps(self):
        if (self.current_player.x, self.current_player.y) in self.start_line:
            if self.current_player.direction == "Est":
                self.current_player.laps += 1
                if self.current_player.laps >= self.nb_laps:
                    self.game_over = True

    def is_finish(self):
        return self.game_over

    def get_winner(self):
        if self.player1.laps >= self.nb_laps:
            return self.player1
        elif self.player2.laps >= self.nb_laps:
            return self.player2
        return None

    def get_loser(self):
        winner = self.get_winner()
        if winner:
            return self.player1 if winner == self.player2 else self.player2
        return None

    def play(self):
        self.load_start_line()
        self.start()
        while not self.is_finish():
            if not self.current_player.inLife:
                self.switch_player()
            bind = self.current_player.play()
            self.one_action(bind)
            self.switch_player()

    def get_karts_positions(self):
        positions = {}
        positions[(self.player1.y, self.player1.x, self.player1.direction)] = "blue"
        positions[(self.player2.y, self.player2.x, self.player2.direction)] = "red"
        return positions