from Game.game_controller import *
from Players.players import *



def training(ai1, ai2, nb_games, nb_epsilon):
        # Train the AIs @ai1 and @ai2 during @nb_games games
        # epsilon decrease every @nb_epsilon games
        training_game = GameModel(15, ai1, ai2, display= False)
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

    for ia_player in ais :
        names += f"{ia_player.name:^15}"
        stats1 += f"{str(ia_player.wins)+'/'+str(ia_player.nb_games):^15}"
        stats2 += f"{f'{ia_player.wins/ia_player.nb_games*100:4.4}'+'%':^15}"

    print(names)
    print(stats1)
    print(stats2)
    print(f"{'-'*4}{'-'*len(ais)*15}")

    all_v_dict = {key : [ia_player.v_function.get(key,0) for ia_player in ais] for key in ais[0].v_function.keys()}
    sorted_v = lambda v_dict : sorted(filter(lambda x : type(x[0])==int ,v_dict.items()))
    for state, values in sorted_v(all_v_dict):
        print(f"{state:2} :", end='')
        for value in values:
            print(f"{value:^15.3f}", end='')
        print()


if __name__ == "__main__":
    
    """
    p1 = Human('test')
    p2 = Human("zigzze")
    
    game = GameControler(p1, p2)
    game.start()
    """

    
    joueur = Player('basique')
    alice = ia_player('Alice')
    bob = ia_player('Bob')
    randy = ia_player('Randy')
    
    test= ia_player('test')
    jsp = Human('jsp')

    """

    training(joueur, test, 1000, 10)

    compare_ai (test)
    
    
    GameControler(jsp, test).start()

    compare_ai(test)
    
    """
    training(bob, alice, 100000, 10)
    training(randy,joueur, 100000, 10)

    bob.wins = 0
    bob.losses = 0
    
    print("test1")

    training(bob,joueur, 100000, 10)
    compare_ai(bob, alice, randy)

    """"
    print("test2")
    training(bob,joueur, 1000000, 10)
    training(alice,joueur, 1000000, 10)
    training(randy,joueur, 1000000, 10)

   
    
    GameControler(bob,jsp).start()
    GameControler(alice,jsp).start()
    """
    
    
