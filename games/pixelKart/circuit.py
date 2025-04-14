from const import * 

class circuit:
    
    def __init__(self,rows:int, cols:int, player1:str , player2:str):
        
        self.rows = rows
        self.cols = cols
        self.player1 = player1
        self.player2 = player2

    def get_current_player(self)->str:
        """
        Retourne le joueur actuel
        """
        return self.current_player

    def moove(self, bind):
        if (bind == 'Nord') and self.can_move(self.current_player.x, self.current_player.y - 1):
            self.move_up()
        elif (bind == 'Sud') and self.can_move(self.current_player.x, self.current_player.y + 1):
            self.move_down()
        elif (bind == 'Ouest') and self.can_move(self.current_player.x - 1, self.current_player.y):
            self.move_left()
        elif (bind == 'Est') and self.can_move(self.current_player.x + 1, self.current_player.y):
            self.move_right()
        else:
            self.current_player.speed = 0

    def move_up(self):
        self.current_player.y -= 1
        
    def move_down(self):
        self.current_player.y += 1

    def move_left(self):
        self.current_player.x -= 1

    def move_right(self):
        self.current_player.x += 1
      
    def can_move(self, x, y):
        return (
                0 <= x < self.rows and
                0 <= y < self.cols
                 )
    
    def type_case(self):
        """
        Retourne le type de case
        """

    def one_action(self):
        """
        Retourne une action
        """

        