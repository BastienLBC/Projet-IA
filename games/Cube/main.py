from Game.game_controller import *

def test_display():
    # Créez deux joueurs
    player1 = Player(name="P1", color="red")
    player2 = HumanPlayer(name="P2", color="green")

    # Initialisez le contrôleur avec les joueurs
    controller = GameController(player1, player2,6)

    # Démarrez le jeu pour tester l'affichage
    controller.start()

if __name__ == "__main__":
    test_display()