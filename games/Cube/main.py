from Game.game_controller import *

if __name__ == "__main__":
    # Créez deux joueurs

    player1 = Player(name="P1", color="red")
    player2 = HumanPlayer(name="P2", color="green")
    player3 = AiPlayer(name="P3", color="blue")

    # Initialisez le contrôleur avec les joueurs
    game = GameController(player1, player3,3)

    # Démarrez le jeu pour tester l'affichage
    train_ai(player1,player3,game,episodes=1000)