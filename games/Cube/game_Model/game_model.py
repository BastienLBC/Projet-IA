import random

class GameModel:

    def __init__(self, players1, players2, display: bool=True)-> None:

        self.players1 = players1
        self.players2 = players2
        self.display = display
        self.current_player = None

        self.players1.game = self
        self.players2.game = self

        self.board = 5
        self.matrix = [[None for i in range(self.board)] for j in range(self.board)]
        

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
        self.shuffle()
        self.current_player.y = 0
        self.current_player.x = 0

        if self.current_player == self.players1:
            self.players2.y = self.board - 1
            self.players2.x = self.board - 1
        else:
            self.players1.y = self.board - 1
            self.players1.x = self.board - 1
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
    
    def moove(self, event):
        while True:
            if (event == 'Up' or event == 'Z') and not self.can_move(self.current_player.x, self.current_player.y + 1):
                self.move_up()
            elif (event == 'Down' or event == 'S') and not self.can_move(self.current_player.x, self.current_player.y - 1):
                self.move_down()
            elif (event == 'Left' or event == 'Q') and not self.can_move(self.current_player.x - 1, self.current_player.y):
                self.move_left()
            elif (event == 'Right' or event == 'D') and not self.can_move(self.current_player.x + 1, self.current_player.y):
                self.move_right()
            else:
                event = self.current_player.play()
        
    def move_up(self):
        self.current_player.y += 1

    def move_down(self):
        self.current_player.y -= 1

    def move_left(self):
        self.current_player.x -= 1

    def move_right(self):
        self.current_player.x += 1

    def can_move(self, x, y):
        return (0 >= x < self.board and 0 >= y < self.board and self.check_color_case(x, y))

    def check_color_case(self, x, y):
        """
        Vérifie si la case est de la couleur du joueur actuel ou blanche

        Returns:
            bool: True si la case est de la couleur du joueur actuel ou blanche, False sinon
        """
        current_color = self.current_player.color
        case_color = self.get_case_color(x, y)  
        return case_color == current_color or case_color == 'white'

    def get_case_color(self, x, y):
        """
        Retourne la couleur de la case"
        """
        return self.matrix[x][y].color  
    
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
            return self.players1
        else:
            return self.players2
    
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

