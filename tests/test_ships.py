from ships import (
    Ship,
    LocationOutsideOfRangeError,
    IncorrectOrientationError,
    UnlocatedShipHitError,
    HitOutsideOfRangeError,
    HitDestroyedSquareError,
    Carrier,
    Destroyer,
    Submarine,
    PatrolBoat,
    Battleship
)
from config import (
    DEFAULT_ORIENTATION,
    BOAT_SIZES
)
import pytest


def test_ship_constructor(monkeypatch):
    def fake_get_uuid():
        return 123

    monkeypatch.setattr("ships.get_uuid", fake_get_uuid)

    ship = Ship(
        size=3
    )

    assert ship._squares == [True, True, True]
    assert ship._uuid == 123
    assert ship._location is None
    assert ship._orientation == DEFAULT_ORIENTATION


def test_ship_squares():
    ship = Ship(
        size=3
    )

    assert ship.squares == [True, True, True]


def test_ship_squares_indexable():
    ship = Ship(
        size=3
    )

    assert ship.squares[0] is True
    assert ship.squares[1] is True
    assert ship.squares[2] is True


def test_ship_size():
    ship = Ship(
        size=3
    )

    assert ship.size == 3


def test_ship_strength():
    ship = Ship(
        size=3
    )
    ship._squares = [True, False, False]
    assert ship.strength == 1


def test_ship_uuid(monkeypatch):
    def fake_get_uuid():
        return 123

    monkeypatch.setattr("ships.get_uuid", fake_get_uuid)

    ship = Ship(
        size=3
    )

    assert ship.uuid == 123


def test_ship_location():
    ship = Ship(
        size=3
    )

    assert ship.location is None

    ship.location = (1, 4)

    assert ship.location == (1, 4)


def test_ship_location_outside_of_range():
    ship = Ship(
        size=3
    )
    with pytest.raises(LocationOutsideOfRangeError):
        ship.location = (10, 4)


def test_ship_orientation():
    ship = Ship(
        size=3
    )

    assert ship.orientation is DEFAULT_ORIENTATION

    ship.orientation = "DOWN"

    assert ship.orientation == "DOWN"


def test_ship_orientation_non_up_down_left_right():
    ship = Ship(
        size=3
    )

    assert ship.orientation is DEFAULT_ORIENTATION

    with pytest.raises(IncorrectOrientationError):
        ship.orientation = "jejdeje"


def test_ship_take_a_hit():
    ship = Ship(
        size=3
    )
    ship.location = (1, 4)

    assert ship.take_a_hit(
        targetIndex=2
    ) == 2

    assert ship._squares == [True, True, False]


def test_ship_take_a_hit_fatal():
    ship = Ship(
        size=3
    )
    ship.location = (1, 4)

    assert ship.take_a_hit(
        targetIndex=2
    ) == 2

    assert ship.take_a_hit(
        targetIndex=1
    ) == 1

    assert ship.take_a_hit(
        targetIndex=0
    ) == 0


def test_ship_take_a_hit_unlocated():
    ship = Ship(
        size=3
    )
    with pytest.raises(UnlocatedShipHitError):
        ship.take_a_hit(
            targetIndex=2
        )


def test_ship_take_a_hit_out_of_range():
    ship = Ship(
        size=3
    )
    ship.location = (1, 4)
    with pytest.raises(HitOutsideOfRangeError):
        ship.take_a_hit(
            targetIndex=3
        )


def test_ship_take_a_hit_already_destroyed():
    ship = Ship(
        size=3
    )
    ship.location = (1, 4)
    with pytest.raises(HitDestroyedSquareError):
        ship.take_a_hit(
            targetIndex=2
        )
        ship.take_a_hit(
            targetIndex=2
        )


def test_carrier():
    ship = Carrier()
    assert ship.size == BOAT_SIZES['Carrier']


def test_battleship():
    ship = Battleship()
    assert ship.size == BOAT_SIZES['Battleship']


def test_destroyer():
    ship = Destroyer()
    assert ship.size == BOAT_SIZES['Destroyer']


def test_submarine():
    ship = Submarine()
    assert ship.size == BOAT_SIZES['Submarine']


def test_patrol_boat():
    ship = PatrolBoat()
    assert ship.size == BOAT_SIZES['PatrolBoat']
