from Game.game_controller import *
from Game.game_models.players import train_ai
if __name__ == "__main__":
    # Créez deux joueurs

    player1 = Player(name="P1", color="red")
    player2 = HumanPlayer(name="P2", color="green")
    player3 = AiPlayer(name="P3", color="blue")
    player4 = AiPlayer(name="P4", color="yellow")
    # Initialisez le contrôleur avec les joueurs
    game = GameController(player3,player4,3)

    # Démarrez le jeu pour tester l'affichage
    train_ai(player3,player4,10000,10)