import pytest
from Game.game_Model.game_model import *

def test_check_enclosure_empty_board():
    game = GameModel("P1", "P2", size=3)
    game.matrix = [
        [{"color": "white"}, {"color": "white"}, {"color": "white"}],
        [{"color": "white"}, {"color": "white"}, {"color": "white"}],
        [{"color": "white"}, {"color": "white"}, {"color": "green"}]
    ]
    game.switch_player = 1
    game.check_enclosure()
    assert game.matrix == [
        [{"color": "white"}, {"color": "white"}, {"color": "white"}],
        [{"color": "white"}, {"color": "white"}, {"color": "white"}],
        [{"color": "white"}, {"color": "white"}, {"color": "green"}]
    ]

def test_check_enclosure_simple_case():
    game = GameModel("P1", "P2", size=3)
    game.matrix = [
        [{"color": "red"}, {"color": "red"}, {"color": "white"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]
    game.switch_player = 1
    game.check_enclosure()
    assert game.matrix == [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]

def test_check_enclosure_no_enclosed_area():
    game = GameModel("P1", "P2", size=3)
    game.matrix = [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "white"}, {"color": "white"}],
        [{"color": "red"}, {"color": "red"}, {"color": "green"}]
    ]
    game.switch_player = 1
    game.check_enclosure()
    assert game.matrix == [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "white"}, {"color": "white"}],
        [{"color": "red"}, {"color": "red"}, {"color": "green"}]
    ]

def test_check_enclosure_multiple_spaces():
    game = GameModel("P1", "P2", size=4)
    game.matrix = [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "white"}, {"color": "white"}, {"color": "red"}],
        [{"color": "red"}, {"color": "white"}, {"color": "red"}, {"color": "red"}]
        [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]
    game.switch_player = 1
    game.check_enclosure()
    assert game.matrix == [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}]
        [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]

def test_check_enclosure_multiple_enclosure():
    game = GameModel("P1", "P2", size=4)
    game.board = [
        [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "white"}],
        [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
        [{"color": "white"}, {"color": "red"}, {"color": "red"}, {"color": "green"}]
        [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]
    game.player_turn = 1
    game.check_enclosure()
    assert game.board == [
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
        [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}]
        [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]
    ]

                
tests = [
    ([[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]],
     1,
     [[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]]),

    ([[{"color": "red"}, {"color": "white"}, {"color": "white"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]],
     1,
     [[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]]),

    ([[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}]],
     1,
     [[{"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}]]),

    ([[{"color": "red"}, {"color": "green"}, {"color": "white"}],
      [{"color": "red"}, {"color": "green"}, {"color": "white"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]],
     2,
     [[{"color": "red"}, {"color": "green"}, {"color": "green"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}],
      [{"color": "red"}, {"color": "green"}, {"color": "green"}]]),

    ([[{"color": "red"}, {"color": "white"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}]],
     1,
     [[{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "red"}, {"color": "green"}]]),

    ([[{"color": "red"}, {"color": "white"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]],
     2,
     [[{"color": "red"}, {"color": "white"}, {"color": "red"}, {"color": "red"}],
      [{"color": "red"}, {"color": "white"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]]),
    
    ([[{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "white"}],
      [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
      [{"color": "white"}, {"color": "red"}, {"color": "green"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]],
     1,
     [[{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "white"}],
      [{"color": "red"}, {"color": "red"}, {"color": "white"}, {"color": "red"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}],
      [{"color": "red"}, {"color": "red"}, {"color": "green"}, {"color": "green"}]]),
    ]


@pytest.mark.parametrize("board,turn,expected", tests)
def test_enclosure(board, turn, expected):
		game = GameModel("P1", "P2", size=len(board))
		game.board = board
		game.switch_player = turn
		game.check_enclosure()
		assert game.board == expected, f"{board} =({turn})=> {game.board}. But expected : {expected} "