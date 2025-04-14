from const import * 
from direction import *

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

    def moove(self):
        x = self.current_player.x
        y = self.current_player.y
        direction = self.current_player.direction
        speed = self.current_player.speed
        
        if speed == 2:
            if (direction == 'Nord') and self.can_move(x, y - 1) :
                self.move_up(1)
                speed = 1
            elif (direction == 'Sud') and self.can_move(x, y + 1) :
                self.move_down(1)
                speed = 1
            elif (direction == 'Ouest') and self.can_move(x - 1, y) :
                self.move_left(1)
                speed = 1
            elif (direction == 'Est') and self.can_move(x + 1, y) :
                self.move_right(1)
                speed = 1
            else:
                self.current_player.speed = 0

        if speed == 1 or speed == -1:
            if (direction == 'Nord') and (self.can_move(x, y - 1) or self.can_move(x, y + 1)):
                self.move_up(speed)
            elif (direction == 'Sud') and (self.can_move(x, y + 1) or self.can_move(x, y - 1)):
                self.move_down(speed)
            elif (direction == 'Ouest') and (self.can_move(x - 1, y) and self.can_move(x +1, y)):
                self.move_left(speed)
            elif (direction == 'Est') and (self.can_move(x + 1, y) and self.can_move(x-1, y)):
                self.move_right(speed)
            else:
                self.current_player.speed = 0

    def move_up(self,speed:int):
        self.current_player.y += speed
        
    def move_down(self,speed:int):
        self.current_player.y += speed

    def move_left(self,speed:int):
        self.current_player.x += speed

    def move_right(self,speed:int):
        self.current_player.x += speed
      
    def can_move(self, x, y):
        return (
                0 <= x < self.rows and
                0 <= y < self.cols
                 )
    
    def type_case(self):
        """
        Retourne le type de case
        """
    
    def accelerate(self):
        """
        Accélère la vitesse du joueur
        """
        if self.current_player.speed <= 2:
            self.current_player.speed += 1

    def decelerate(self):
        """
        Ralentit la vitesse du joueur
        """
        if self.current_player.speed > -1:
            self.current_player.speed -= 1
    
    def turn_left(self):
        """
        Tourne le joueur à gauche
        """
        direction = self.current_player.direction 

        if direction == "Nord":
            self.current_player.direction = "Ouest"
        elif direction == "Est":
            self.current_player.direction = "Nord"
        elif direction == "Sud":
            self.current_player.direction = "Est"
        else :
            self.current_player.direction = "Sud"
    
    def turn_right(self):
        """
        Tourne le joueur à droite
        """
        direction = self.current_player.direction

        if direction == "Nord":
            self.current_player.direction = "Est"
        elif direction == "Est":
            self.current_player.direction = "Sud"
        elif direction == "Sud":
            self.current_player.direction = "Ouest"
        else :
            self.current_player.direction = "Nord"

    def one_action(self,bind):
        """
        Retourne une action
        """
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
        
