from const import *
import random

class circuit:
    
    def __init__(self,rows:int, cols:int, player1:str , player2:str, gp:str=None):
        
        self.rows = rows
        self.cols = cols
        self.player1 = player1
        self.player2 = player2
        self.start_line = [] #liste de tuple de positions ex:[(0,0),(0,1),(0,2)]
        self.nb_laps = 1 #nombre de tours à faire
        self.circuit = gp
        self.current_player = None

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

    def speed_limiter(self):
        """
        modifie la vitesse du joueur en fonction de la case
        """
        if self.type_case() == 'ROAD':
            self.current_player.speed = 2
        if self.type_case() == "GRASS":
            self.current_player.speed = 1

        if self.type_case() == "WALL":
            self.current_player.speed = 0
            self.current_player.losses += 1
            #le faire arrêter  - MORT

    def load_start_line(self):
        """
        Charge le circuit et trouve la ligne d'arrivée
        """
        grid = [list(row) for row in self.circuit.split(',')]
        self.start_line = []

        # Trouve toutes les cases "F"
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == PIXEL_TYPES["FINISH"]["letter"]:
                    self.start_line.append((x, y))

    def start(self):
        """
        Positionne les joueurs aleatoirement sur la ligne d'arrivée, dirigés vers l'est
        """
        pos1_index = random.randint(0, len(self.start_line) - 1)
        x1, y1 = self.start_line[pos1_index]  #pour décomposer le tple
        self.player1.x = x1
        self.player1.y = y1
        self.player1.direction = 'Est'
        self.player1.speed = 0

        pos2_index = random.randint(0, len(self.start_line) - 1)
        x2, y2 = self.start_line[pos2_index]
        self.player2.x = x2
        self.player2.y = y2
        self.player2.direction = 'Est'
        self.player2.speed = 0

        # SI PAS TUPLE EN ENTREE :
        #----------------------------------
        # self.player1.x = self.start_line[random.randint(0,len(self.start_line)-1)]
        # self.player1.y = self.start_line[random.randint(0,len(self.start_line)-1)]
        # self.player1.direction = 'Est'
        # self.player1.speed = 0
        #
        # self.player2.x = self.start_line[random.randint(0, len(self.start_line) - 1)]
        # self.player2.y = self.start_line[random.randint(0, len(self.start_line) - 1)]
        # self.player2.direction = 'Est'
        # self.player2.speed = 0
        #----------------------------------

    def finish_line(self):
        """
        Vérifie si le joueur a franchi la ligne d'arrivée,
        dans le bon sens (vers l'est) et il a fait le bon nombre de tours
        on lui ajoute une victoire(et fini la partie), sinon on lui ajoute un tour à son compteur
        """

        if self.current_player.x in self.start_line :
            if self.current_player.direction == 'Est':
                if self.current_player.laps == self.nb_laps:
                    self.current_player.wins += 1
                    #PARTIE FINIE (jsp encore comment faire)
                else:
                    self.current_player.laps += 1

