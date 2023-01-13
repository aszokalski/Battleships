from players import Player
from ships import Ship, get_default_ship_set


def test_player_constructor_1():
    ship = Ship(size=4)
    player = Player(name="Adam", ships=[ship])

    assert player._ships == {ship.uuid: ship}
    assert player._name == "Adam"
    assert player._board._player == player


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
