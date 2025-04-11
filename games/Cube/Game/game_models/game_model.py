import random
import queue

class GameModel:

    def __init__(self, players1, players2,board, display: bool=True) -> None:

        self.players1 = players1
        self.players2 = players2
        self.display = display
        self.current_player = None
        self.board = board
        self.size = board

        self.players1.game = self
        self.players2.game = self

    
        self.matrix = [[{"color": "white"} for i in range(self.board)] for j in range(self.board)]
        if self.is_ai(players1):
            players1.board = self
        if self.is_ai(players2):
            players2.board = self

        self.reset()

    def is_ai(self, player):
        from Game.game_models.players import AiPlayer  # Importation différée
        return isinstance(player, AiPlayer)

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
        if (bind == 'UP') and self.can_move(self.current_player.x, self.current_player.y - 1):
            self.move_up()
        elif (bind == 'DOWN') and self.can_move(self.current_player.x, self.current_player.y + 1):
            self.move_down()
        elif (bind == 'LEFT') and self.can_move(self.current_player.x - 1, self.current_player.y):
            self.move_left()
        elif (bind == 'RIGHT') and self.can_move(self.current_player.x + 1, self.current_player.y):
            self.move_right()
        self.check_enclosure()

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
        return self.players1 if self.players1.score > self.players2.score else self.players2
        
    def get_loser(self)->str:
        """
        Retourne le joueur perdant

        Returns:
            Player: joueur perdant
        """
        return self.players2 if self.players1.score > self.players2.score else self.players1
    
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
            
        winner = self.get_winner()
        loser = self.get_loser()
        winner.win()
        loser.lose()
            
    def get_matrix_state(self):
        """
        Retourne une représentation de l'état actuel de la matrice.
        """
        return [[cell["color"] for cell in row] for row in self.matrix]

    def get_board_state(self):
        """
        Retourne une représentation de l'état actuel du plateau.
        """
        return {
            "players1": {"x": self.players1.x, "y": self.players1.y, "score": self.players1.score},
            "players2": {"x": self.players2.x, "y": self.players2.y, "score": self.players2.score},
        }

    def check_enclosure(self):
        """
        Vérifie si un joueur a enfermé des cases blanches.
        Convertit toutes les cases blanches inaccessibles en couleur du joueur actuel.
        """
        player = self.current_player
        opponent = self.players1 if self.current_player == self.players2 else self.players2

        reachable = [[False for _ in range(self.board)] for _ in range(self.board)]
        queue = [(player.x, player.y)]

        while queue:
            x, y = queue.pop(0)  
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.board and 0 <= ny < self.board and
                    not reachable[nx][ny] and 
                    (self.matrix[nx][ny]["color"] == "white" or self.matrix[nx][ny]["color"] == player.color)):
                    reachable[nx][ny] = True
                    queue.append((nx, ny))  

        for x in range(self.board):
            for y in range(self.board):
                if self.matrix[x][y]["color"] == "white" and not reachable[x][y]:
                    self.matrix[x][y]["color"] = opponent.color  
                    opponent.score += 1  

