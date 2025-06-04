import pytest
from Game.game_models.game_model import *
from Game.game_models.players import *

def test_check_enclosure_empty_board():
    player1 = Player("P1", "red")  # Create a Player object
    player2 = Player("P2", "green")  # Create a Player object
    game = GameModel(player1, player2, board=3)
    game.matrix = [
        [{"color": "white"}, {"color": "white"}, {"color": "white"}],
        [{"color": "white"}, {"color": "white"}, {"color": "white"}],
        [{"color": "white"}, {"color": "white"}, {"color": "green"}]
    ]
    game.current_player = game.players1
    game.check_enclosure()
    assert game.matrix == [
        [{"color": "white"}, {"color": "white"}, {"color": "white"}],
        [{"color": "white"}, {"color": "white"}, {"color": "white"}],
        [{"color": "white"}, {"color": "white"}, {"color": "green"}]
    ]

def test_check_enclosure_simple_case():
    player1 = Player("P1", "red")  # Create a Player object
    player2 = Player("P2", "green")  # Create a Player object
    game = GameModel(player1, player2, board=3)
    game.matrix = [
        [{"color": "red"}, {"color": "red"}, {"color": "white"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]
    game.current_player = game.players2
    game.check_enclosure()
    
    assert game.matrix == [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]

def test_check_enclosure_no_enclosed_area():
    player1 = Player("P1", "red")  # Create a Player object
    player2 = Player("P2", "green")  # Create a Player object
    game = GameModel(player1, player2, board=3)
    game.matrix = [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "white"}, {"color": "white"}],
        [{"color": "red"}, {"color": "red"}, {"color": "green"}]
    ]
    game.current_player = game.players1
    game.check_enclosure()
    assert game.matrix == [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "white"}, {"color": "white"}],
        [{"color": "red"}, {"color": "red"}, {"color": "green"}]
    ]

def test_check_enclosure_multiple_spaces():
    player1 = Player("P1", "red")  # Create a Player object
    player2 = Player("P2", "green")  # Create a Player object
    game = GameModel(player1, player2, board=4)
    game.matrix = [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "white"}, {"color": "white"}, {"color": "red"}],
        [{"color": "red"}, {"color": "white"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]
    game.current_player = game.players2
    game.check_enclosure()
    assert game.matrix == [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]

def test_check_enclosure_multiple_enclosure():
    player1 = Player("P1", "red")  # Create a Player object
    player2 = Player("P2", "green")  # Create a Player object
    game = GameModel(player1, player2, board=4)
    game.matrix = [
        [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "white"}],
        [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
        [{"color": "white"}, {"color": "red"}, {"color": "red"}, {"color": "green"}],
        [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]
    game.current_player = game.players2
    game.check_enclosure()
    assert game.matrix == [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}],
        [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]

                
tests = [
    ([[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]
      ],
     2,
     [[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]
      ]
      ),

    ([[{"color": "red"}, {"color": "white"}, {"color": "white"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]
      ],
     2,
     [[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]
      ]
      ),

    ([[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}]
      ],
     2,
     [[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}]
      ]
      ),

    ([[{"color": "red"}, {"color": "green"}, {"color": "white"}],
      [{"color": "red"}, {"color": "green"}, {"color": "white"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]
      ],
     1,
     [[{"color": "red"}, {"color": "green"}, {"color": "green"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]
      ]
      ),

    ([[{"color": "red"}, {"color": "white"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}]
      ],
     2,
     [[{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}]
      ]
      ),

    ([[{"color": "red"}, {"color": "white"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
      ],
     1,
     [[{"color": "red"}, {"color": "white"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
      ]
      ),
    
    ([[{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "white"}],
      [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
      [{"color": "white"}, {"color": "red"}, {"color": "green"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
      ],
     2,
     [[{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "white"}],
      [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
      ]
      ),
    ]


@pytest.mark.parametrize("board_matrix,turn,expected", tests)
def test_enclosure(board_matrix, turn, expected):
    player1 = HumanPlayer(name="P1", color="red")
    player2 = HumanPlayer(name="P2", color="green")
    game = GameModel(player1, player2, board=len(board_matrix))
    import copy
    game.matrix = copy.deepcopy(board_matrix)  # Prevent side effects
    # Position players in opposite corners to avoid random placement
    game.players1.x = 0
    game.players1.y = 0
    game.players2.x = len(board_matrix) - 1
    game.players2.y = len(board_matrix) - 1
    game.current_player = game.players1 if turn == 1 else game.players2
    

    game.check_enclosure()


    assert game.matrix == expected, f"{board_matrix} =({turn})=> {game.matrix}. But expected : {expected}"
