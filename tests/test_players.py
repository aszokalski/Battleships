from players import Player, AIPlayer, EnemyUnsetError
from ships import Ship, get_default_ship_set
from boards import Board
from utils import AttackResult
import config
import pytest
import numpy as np


def test_player_constructor_1():
    ship = Ship(size=4)
    player = Player(name="Adam", ships=[ship])

    assert player._ships == {ship.uuid: ship}
    assert player._name == "Adam"
    assert player._board._player == player
    assert player._enemy is None
    assert player._fleet_strength == 4
    assert player._side == config.DEFAULT_PLAYER_SIDE


def test_player_constructor_2():
    player = Player()
    default_ship_set = get_default_ship_set()
    for (player_ship_key, player_ship), expected_ship in zip(
        player._ships.items(), default_ship_set
    ):
        assert type(player_ship) == type(expected_ship)
        assert player_ship_key == player_ship.uuid

    assert player._name == "Unnamed"


def test_player_ui():
    class fake_CLI:
        def __init__(self):
            pass

    player = Player(ui=fake_CLI())

    assert type(player._ui) == fake_CLI


def test_player_name():
    player = Player()

    assert player.name == "Unnamed"


def test_player_ships():
    ship = Ship(size=4)
    player = Player(ships=[ship])

    assert player.ships == {ship.uuid: ship}


def test_player_side():
    player = Player(side=1)

    assert player.side == 1


def test_player_board():
    player = Player()

    assert player.board._player == player


def test_player_set_enemy():
    player = Player()
    enemy = Player()
    player.set_enemy(enemy)

    assert player._enemy == enemy


def test_player_enemy_board():
    player = Player()
    enemy = Player()
    player._enemy = enemy

    assert player.enemy_board._player == enemy


def test_player_enemy_board_enemy_None():
    player = Player()

    with pytest.raises(EnemyUnsetError):
        player.enemy_board


def test_player_fleet_strength():
    ship = Ship(size=4)
    player = Player(ships=[ship])
    player.fleet_strength -= 1

    assert player.fleet_strength == 3


def test_player_cli_initialize_board():
    class fake_CLI:
        def __init__(self):
            pass

        def get_move_ship_data(self, ship: Ship, board: Board):
            return (
                *board.get_possible_locations(ship.size, ship.orientation)[0],
                ship.orientation,
            )

    player = Player(ui=fake_CLI())
    player.initialize_board()

    # Check if the number of occupied squares
    # on the matrix is equal to the sum of the
    # ship sizes
    x = player.board._matrix
    assert np.count_nonzero(x != None) == player.fleet_strength  # noqa: E711


def test_ai_player_initialize_board():
    player = AIPlayer()
    player.initialize_board()

    # Check if the number of occupied squares
    # on the matrix is equal to the sum of the
    # ship sizes
    x = player.board._matrix
    assert np.count_nonzero(x != None) == player.fleet_strength  # noqa: E711


def test_player_cli_attack_enemy():
    class fake_CLI:
        def __init__(self):
            pass

        def get_location(self, *args):
            return (2, 3)

    player = Player(ui=fake_CLI())
    enemy = Player()
    player.set_enemy(enemy)
    enemy.board.add_ship(list(enemy.ships.keys())[0], (2, 3), "UP")

    assert player.attack_enemy() == AttackResult.HIT


def test_ai_player_attack_enemy():
    player = AIPlayer()
    enemy = Player()
    player.set_enemy(enemy)
    enemy.board.add_ship(list(enemy.ships.keys())[0], (2, 3), "UP")

    player.attack_enemy()
    # TODO: Add a test for the AIPlayer attack
