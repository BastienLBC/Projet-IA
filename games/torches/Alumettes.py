from Game.game_controller import *
from Players.players import Human, ia_player,Player

if __name__ == "__main__":
    joueur = Player('Joueur')
    alice = ia_player('alice')
    bob = ia_player('bob')
    randy = ia_player('randy')


    # Entraînement de Alice et Bob
    training(alice, bob, 1000, 10)

    # Entraînement de Randy contre le joueur basique
    training(randy, joueur, 1000, 10)
    """"
    # Remettre les stats de Bob à 0
    reset_stats(bob)

    # Faire jouer Bob contre le joueur basique
    training([bob, joueur], 1000, 10)

    # Comparer les stats et la value-function des IA
    compare_stats_and_value_function([alice, bob, randy])

    # Relancer les mêmes tests avec 100.000 parties
    train([alice, bob], 100000, 10)
    train([randy, joueur], 100000, 10)
    reset_stats(bob)
    train([bob, joueur], 100000, 10)
    compare_stats_and_value_function([alice, bob, randy])
    """