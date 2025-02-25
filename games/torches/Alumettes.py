from Game.game_controller import *
from Players.players import *

def training(ai1, ai2, nb_games, nb_epsilon):
    # Train the AIs @ai1 and @ai2 during @nb_games games
    # epsilon decrease every @nb_epsilon games
    training_game = GameModel(12, [ai1, ai2], display = False)
    for i in range(0, nb_games):
        if i % nb_epsilon == 0:
            if type(ai1)==ia_player : ai1.next_epsilon()
            if type(ai2)==ia_player : ai2.next_epsilon()

        training_game.play()
        if type(ai1)==ia_player : ai1.train()
        if type(ai2)==ia_player : ai2.train()

        training_game.reset()

def compare_ai(*ais):
    # Print a comparison between the @ais
    names = f"{'':4}"
    stats1 = f"{'':4}"
    stats2 = f"{'':4}"

    for ai in ais :
        names += f"{ai.name:^15}"
        stats1 += f"{str(ai.nb_wins)+'/'+str(ai.nb_games):^15}"
        stats2 += f"{f'{ai.nb_wins/ai.nb_games*100:4.4}'+'%':^15}"

    print(names)
    print(stats1)
    print(stats2)
    print(f"{'-'*4}{'-'*len(ais)*15}")

    all_v_dict = {key : [ai.V.get(key,0) for ai in ais] for key in ais[0].V.keys()}
    sorted_v = lambda v_dict : sorted(filter(lambda x : type(x[0])==int ,v_dict.items()))
    for state, values in sorted_v(all_v_dict):
        print(f"{state:2} :", end='')
        for value in values:
            print(f"{value:^15.3}", end='')
        print()

if __name__ == "__main__":
    joueur = Player('Joueur')
    alice = ia_player('alice')
    bob = ia_player('bob')
    randy = ia_player('randy')

    
    # Entraînement de Alice et Bob
    
    training(alice,bob,1000,10)
    # Entraînement de Randy contre le joueur basique
    training([randy, joueur], 1000, 10)

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