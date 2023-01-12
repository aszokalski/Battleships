from players import Player
from ships import Ship


def test_player_constructor_1():
    ship = Ship(size=4)
    player = Player(ships=[ship])

    assert player.ships == {ship.uuid: ship}


def test_player_constructor_2():
    player = Player()

    assert player.ships == {}
