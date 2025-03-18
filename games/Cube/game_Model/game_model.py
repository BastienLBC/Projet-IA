import random
from games.Cube.game_Model.players import Player

class GameModel:

    def __init__(self, players1, players2, display: bool=True) -> None:
        self.players1 = players1
        self.players2 = players2
        self.display = display
        self.current_player = None

        self.players1.game = self
        self.players2.game = self

        self.board_size = 5
        self.board = self.create_board()

        self.shuffle()

    def shuffle(self) -> None:
        self.current_player = random.choice([self.players1, self.players2])

    def switch_player(self) -> None:
        self.current_player = self.players1 if self.current_player == self.players2 else self.players2

    def get_current_player(self) -> str:
        return self.current_player

    def moove(self, event):
        if event.keysym == 'UP' or event.keysym == 'Z':
            self.moove_up()
        elif event.keysym == 'DOWN' or event.keysym == 'S':
            self.moove_down()
        elif event.keysym == 'LEFT' or event.keysym == 'Q':
            self.moove_left()
        elif event.keysym == 'RIGHT' or event.keysym == 'D':
            self.moove_right()

    def moove_up(self):
        if self.current_player.y > 0 and self.check_color_case(self.current_player.x, self.current_player.y - 1):
            self.current_player.y -= 1

    def moove_down(self):
        if self.current_player.y < self.board_size - 1 and self.check_color_case(self.current_player.x, self.current_player.y + 1):
            self.current_player.y += 1

    def moove_left(self):
        if self.current_player.x > 0 and self.check_color_case(self.current_player.x - 1, self.current_player.y):
            self.current_player.x -= 1

    def moove_right(self):
        if self.current_player.x < self.board_size - 1 and self.check_color_case(self.current_player.x + 1, self.current_player.y):
            self.current_player.x += 1

    def check_color_case(self, x, y):
        current_color = self.current_player.color
        case_color = self.get_case_color(x, y)
        return case_color == current_color or case_color == 'white'

    def get_case_color(self, x, y):
        return self.board[x][y].color if isinstance(self.board[x][y], Player) else self.board[x][y]

    def create_board(self) -> list:
        size = self.board_size
        board_grid = [['white' for _ in range(size)] for _ in range(size)]
        board_grid[0][0] = self.players1
        board_grid[size - 1][size - 1] = self.players2
        return board_grid

    def get_winner(self) -> Player:
        return self.players1 if self.players1.score > self.players2.score else self.players2

    def get_looser(self) -> Player:
        return self.players1 if self.players1.score < self.players2.score else self.players2

    def is_finished(self) -> bool:
        return self.players1.score + self.players2.score == (self.board_size - 1) * (self.board_size - 1)

    def play(self) -> None:
        pass