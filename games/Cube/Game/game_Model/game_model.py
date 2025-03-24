import random

class GameModel:

    def __init__(self, players1, players2,board, display: bool=True) -> None:

        self.players1 = players1
        self.players2 = players2
        self.display = display
        self.current_player = None
        self.board = board

        self.players1.game = self
        self.players2.game = self

    
        self.matrix = [[{"color": "white"} for i in range(self.board)] for j in range(self.board)]
        

        self.reset()

    def shuffle(self)->None:
        """
        Selecte aléatoirement un joueur pour commencer
        """
        self.current_player = random.choice([self.players1, self.players2])

    def reset(self)->None:
        """
        Réinitialise le jeu
        """
        self.matrix = [[{"color": "white"} for i in range(self.board)] for j in range(self.board)]

        self.shuffle()

        self.current_player.y = 0
        self.current_player.x = 0
        self.matrix[0][0]["color"] = self.current_player.color

        if self.current_player == self.players1:
            other_player = self.players2
        else:
            other_player = self.players1
        other_player.y = self.board - 1
        other_player.x = self.board - 1
        self.matrix[self.board - 1][self.board - 1]["color"] = other_player.color

        self.players1.score = 1
        self.players2.score = 1

    def switch_player(self)->None:
        """
        Inverse le joueur courant
        """
        self.current_player = self.players1 if self.current_player == self.players2 else self.players2

    def get_current_player(self)->str:
        """
        Retourne le joueur actuel

        Returns:
            Player: joueur actuel
        """
        return self.current_player

    def moove(self, bind):
        if (bind == 'Up' or bind == 'Z' or bind == 'z') and self.can_move(self.current_player.x, self.current_player.y - 1):
            self.move_up()
        elif (bind == 'Down' or bind == 'S' or bind == 's') and self.can_move(self.current_player.x, self.current_player.y + 1):
            self.move_down()
        elif (bind == 'Left' or bind == 'Q' or bind == 'q') and self.can_move(self.current_player.x - 1, self.current_player.y):
            self.move_left()
        elif (bind == 'Right' or bind == 'D' or bind == 'd') and self.can_move(self.current_player.x + 1, self.current_player.y):
            self.move_right()

    def move_up(self):
        self.current_player.y -= 1
        if self.get_case_color(self.current_player.x, self.current_player.y) == 'white':
            self.current_player.score += 1
            self.matrix[self.current_player.x][self.current_player.y]["color"] = self.current_player.color

    def move_down(self):
        self.current_player.y += 1
        if self.get_case_color(self.current_player.x, self.current_player.y) == 'white':
            self.current_player.score += 1
            self.matrix[self.current_player.x][self.current_player.y]["color"] = self.current_player.color

    def move_left(self):
        self.current_player.x -= 1
        if self.get_case_color(self.current_player.x, self.current_player.y) == 'white':
            self.current_player.score += 1     
            self.matrix[self.current_player.x][self.current_player.y]["color"] = self.current_player.color

    def move_right(self):
        self.current_player.x += 1
        if self.get_case_color(self.current_player.x, self.current_player.y) == 'white':
            self.current_player.score += 1
            self.matrix[self.current_player.x][self.current_player.y]["color"] = self.current_player.color

    def can_move(self, x, y):
        return (
                0 <= x < self.board and
                0 <= y < self.board and
                (self.get_case_color(x, y) == 'white' or
                 self.get_case_color(x, y) == self.current_player.color)
                 )

    def get_case_color(self, x, y):
        """
        Retourne la couleur de la case
        """
        return self.matrix[x][y]["color"]

    def get_winner(self)->str:
        """
        Retourne le joueur gagnant

        Returns:
            Player: joueur gagnant
        """
        if self.players1.score > self.players2.score:
            return self.players1
        else:
            return self.players2
        
    def get_loser(self)->str:
        """
        Retourne le joueur perdant

        Returns:
            Player: joueur perdant
        """
        if self.players1.score < self.players2.score:
            return self.players2
        else:
            return self.players1
    
    def is_finished(self)->bool:
        """
        Vérifie si la partie est terminée

        Returns:
            bool: True si la partie est terminée, False sinon
        """
        return self.players1.score + self.players2.score == self.board * self.board
        
    def play(self) -> None:
        """
        Lance le jeu et gère le déroulement du tour.
        """
        while not self.is_finished():
            
            self.moove(self.current_player.play())            
            self.switch_player()
            self.check_enclosure()
            

    def check_enclosure(self):
        """
        Vérifie si un joueur a enfermé des cases blanches.
        Convertit toutes les cases blanches inaccessibles en couleur du joueur actuel.
        """
        player = self.current_player
        opponent = self.players1 if self.current_player == self.players2 else self.players2
        
        reachable = [[False for _ in range(self.board)] for _ in range(self.board)]
        queue = [(player.x, player.y)]
        reachable[player.x][player.y] = True

        while queue:
            x, y = queue.pop(0) 
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.board and 
                   0 <= ny < self.board and 
                   self.matrix[nx][ny]["color"] != opponent.color):
                        reachable[nx][ny] = True
                        queue.append((nx, ny))

        for x in range(self.board):
            for y in range(self.board):
                if not reachable[x][y] and self.matrix[x][y]["color"] == "white":
                    self.matrix[x][y]["color"] = opponent.color
                    opponent.score += 1