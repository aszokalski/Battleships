from game import Game
from players import Player, AIPlayer
import numpy as np


def test_game_constructor():
    player = Player(side=0, name="Adam")
    enemy = Player(side=1, name="AI")

    game = Game(player, enemy)

    assert game._playerA._enemy == enemy
    assert game._playerB._enemy == player


def test_game_initialize_boards():
    player = AIPlayer(side=0, name="Adam")
    enemy = AIPlayer(side=1, name="AI")

    game = Game(player, enemy)
    game.initialize_boards()

    x = player.board._matrix
    assert np.count_nonzero(x != None) == player.fleet_strength  # noqa: E711

    y = enemy.board._matrix
    assert np.count_nonzero(y != None) == enemy.fleet_strength  # noqa: E711


def test_game_start():
    player = AIPlayer(side=0, name="AI1")
    enemy = AIPlayer(side=1, name="AI2")

    game = Game(player, enemy)
    game.initialize_boards()
    result = game.start()

    assert player.fleet_strength == 0 or enemy.fleet_strength == 0
    assert result == (player.fleet_strength > enemy.fleet_strength)
