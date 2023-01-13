from players import Player, EnemyUnsetError
from ships import Ship, get_default_ship_set
import pytest


def test_player_constructor_1():
    ship = Ship(size=4)
    player = Player(name="Adam", ships=[ship])

    assert player._ships == {ship.uuid: ship}
    assert player._name == "Adam"
    assert player._board._player == player
    assert player._enemy is None
    assert player._fleet_strength == 4


def test_player_constructor_2():
    player = Player()
    default_ship_set = get_default_ship_set()
    for (player_ship_key, player_ship), expected_ship in zip(
        player._ships.items(), default_ship_set
    ):
        assert type(player_ship) == type(expected_ship)
        assert player_ship_key == player_ship.uuid

    assert player._name == "Unnamed"


def test_player_name():
    player = Player()

    assert player.name == "Unnamed"


def test_player_ships():
    ship = Ship(size=4)
    player = Player(ships=[ship])

    assert player.ships == {ship.uuid: ship}


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
