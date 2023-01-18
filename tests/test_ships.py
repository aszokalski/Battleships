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
    Battleship,
    get_default_ship_set,
)
import pytest
import config


def test_ship_constructor(monkeypatch):
    def fake_get_uuid():
        return 123

    monkeypatch.setattr("ships.get_uuid", fake_get_uuid)

    ship = Ship(size=3)

    assert ship._squares == [True, True, True]
    assert ship._uuid == 123
    assert ship._location is None
    assert ship._orientation == config.DEFAULT_ORIENTATION
    assert ship._under_edition is True


def test_ship_squares():
    ship = Ship(size=3)

    assert ship.squares == [True, True, True]


def test_ship_squares_indexable():
    ship = Ship(size=3)

    assert ship.squares[0] is True
    assert ship.squares[1] is True
    assert ship.squares[2] is True


def test_ship_size():
    ship = Ship(size=3)

    assert ship.size == 3


def test_ship_strength():
    ship = Ship(size=3)
    ship._squares = [True, False, False]
    assert ship.strength == 1


def test_ship_uuid(monkeypatch):
    def fake_get_uuid():
        return 123

    monkeypatch.setattr("ships.get_uuid", fake_get_uuid)

    ship = Ship(size=3)

    assert ship.uuid == 123


def test_ship_location():
    ship = Ship(size=3)

    assert ship.location is None

    ship.location = (1, 4)

    assert ship.location == (1, 4)


def test_ship_under_edition():
    ship = Ship(size=3)
    ship.under_edition = False
    assert ship.under_edition is False


def test_ship_under_edition_type_error():
    ship = Ship(size=3)
    with pytest.raises(TypeError):
        ship.under_edition = 3


def test_ship_location_outside_of_range():
    ship = Ship(size=3)
    with pytest.raises(LocationOutsideOfRangeError):
        ship.location = (10, 4)


def test_ship_location_none():
    ship = Ship(size=3)
    ship.location = None
    assert ship.location is None


def test_ship_orientation():
    ship = Ship(size=3)

    assert ship.orientation is config.DEFAULT_ORIENTATION

    ship.orientation = "DOWN"

    assert ship.orientation == "DOWN"


def test_ship_orientation_non_up_down_left_right():
    ship = Ship(size=3)

    assert ship.orientation is config.DEFAULT_ORIENTATION

    with pytest.raises(IncorrectOrientationError):
        ship.orientation = "jejdeje"


def test_ship_take_a_hit():
    ship = Ship(size=3)
    ship.location = (1, 4)

    assert ship.take_a_hit(targetIndex=2) == 2

    assert ship._squares == [True, True, False]


def test_ship_take_a_hit_fatal():
    ship = Ship(size=3)
    ship.location = (1, 4)

    assert ship.take_a_hit(targetIndex=2) == 2

    assert ship.take_a_hit(targetIndex=1) == 1

    assert ship.take_a_hit(targetIndex=0) == 0


def test_ship_take_a_hit_unlocated():
    ship = Ship(size=3)
    with pytest.raises(UnlocatedShipHitError):
        ship.take_a_hit(targetIndex=2)


def test_ship_take_a_hit_out_of_range():
    ship = Ship(size=3)
    ship.location = (1, 4)
    with pytest.raises(HitOutsideOfRangeError):
        ship.take_a_hit(targetIndex=3)


def test_ship_take_a_hit_already_destroyed():
    ship = Ship(size=3)
    ship.location = (1, 4)
    with pytest.raises(HitDestroyedSquareError):
        ship.take_a_hit(targetIndex=2)
        ship.take_a_hit(targetIndex=2)


def test_carrier():
    ship = Carrier()
    assert ship.size == config.BOAT_SIZES["Carrier"]


def test_battleship():
    ship = Battleship()
    assert ship.size == config.BOAT_SIZES["Battleship"]


def test_destroyer():
    ship = Destroyer()
    assert ship.size == config.BOAT_SIZES["Destroyer"]


def test_submarine():
    ship = Submarine()
    assert ship.size == config.BOAT_SIZES["Submarine"]


def test_patrol_boat():
    ship = PatrolBoat()
    assert ship.size == config.BOAT_SIZES["PatrolBoat"]


def test_get_default_ship_class_set():
    pre_val = config.DEFAULT_SHIP_SET

    config.DEFAULT_SHIP_SET = [(2, "Carrier"), (1, "Battleship")]

    default_set = get_default_ship_set()

    assert isinstance(default_set[0], Carrier)
    assert isinstance(default_set[1], Carrier)
    assert isinstance(default_set[2], Battleship)

    # setting it back to default because other tests use it
    config.DEFAULT_SHIP_SET = pre_val
