from boards import (
    Board,
    Cell,
    DoubleDestructionError,
    CellAlreadyOccupiedError,
    ShipDoesNotExistError,
    UnlocatedShipRemovalError,
)
from players import Player
from ships import Ship, HitDestroyedSquareError, LocationOutsideOfRangeError
from utils import AttackResult
import config
import pytest
import numpy as np
from itertools import chain


def test_cell_constructor():
    cell = Cell(shipUUID=57, squareIndex=2, alive=True)

    assert cell.shipUUID == 57
    assert cell.squareIndex == 2
    assert cell._alive is True


def test_cell_destroy():
    cell = Cell(shipUUID=57, squareIndex=2, alive=True)
    cell.destroy()

    assert cell.alive is False


def test_cell_repr():
    cell = Cell(shipUUID=57, squareIndex=2, alive=True)

    assert cell.__repr__() == "Cell(57, 2, True)"


def test_cell_destroy_dead():
    cell = Cell(shipUUID=57, squareIndex=2, alive=False)

    with pytest.raises(DoubleDestructionError):
        cell.destroy()


def test_board_constructor():
    player = Player()
    board = Board(player=player)
    board_size = config.BOARD_SIZE
    empty_matrix = np.array([None for _ in range(board_size**2)]).reshape(
        board_size, board_size
    )

    assert board._player == player
    assert board._size == board_size
    assert np.array_equal(board._matrix, empty_matrix)


def test_board_size():
    player = Player()
    board = Board(player=player)

    assert board.size == config.BOARD_SIZE


def test_board_player():
    player = Player()
    board = Board(player=player)

    assert board.player == player


def test_board_calculate_square_locations_UP_partial_surround():
    player = Player()
    board = Board(player=player)

    square_locations = board.calculate_square_locations(
        start_location=(0, 0), orientation="UP", size=5
    )

    # Square locations of the ship
    assert square_locations[0] == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]

    # Square locations of the surrounding area
    assert square_locations[1] == [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
    ]


def test_board_calculate_square_locations_DOWN_partial_surround():
    player = Player()
    board = Board(player=player)

    square_locations = board.calculate_square_locations(
        start_location=(0, 4), orientation="DOWN", size=5
    )

    assert square_locations[0] == [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    assert square_locations[1] == [
        (0, 5),
        (0, 4),
        (0, 3),
        (0, 2),
        (0, 1),
        (0, 0),
        (1, 5),
        (1, 4),
        (1, 3),
        (1, 2),
        (1, 1),
        (1, 0),
    ]


def test_board_calculate_square_locations_RIGHT_full_suround():
    player = Player()
    board = Board(player=player)

    square_locations = board.calculate_square_locations(
        start_location=(1, 1), orientation="RIGHT", size=5
    )

    assert square_locations[0] == [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    assert set(square_locations[1]) == set([(x, y) for x in range(7) for y in range(3)])


def test_board_calculate_square_locations_LEFT_partial_surround():
    player = Player()
    board = Board(player=player)

    assert board.calculate_square_locations(
        start_location=(4, 0), orientation="LEFT", size=5
    )[0] == [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]

    square_locations = board.calculate_square_locations(
        start_location=(4, 1), orientation="LEFT", size=5
    )

    assert square_locations[0] == [(4, 1), (3, 1), (2, 1), (1, 1), (0, 1)]
    assert set(square_locations[1]) == set(
        [(x, y) for x in range(5, -1, -1) for y in range(3)]
    )


def test_board_calculate_square_locations_sticking_out_1():
    player = Player()
    board = Board(player=player)

    with pytest.raises(LocationOutsideOfRangeError):
        board.calculate_square_locations(
            start_location=(3, 0), orientation="LEFT", size=5
        )


def test_board_calculate_square_locations_sticking_out_2():
    player = Player()
    board = Board(player=player)

    with pytest.raises(LocationOutsideOfRangeError):
        board.calculate_square_locations(
            start_location=(7, 0), orientation="RIGHT", size=5
        )


def test_board_add_ship():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)

    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")

    assert isinstance(board._matrix[3, 4], Cell)
    assert board._matrix[3, 4].shipUUID == ship.uuid
    assert board._matrix[3, 4].squareIndex == 0
    assert board._matrix[3, 4].alive is True

    assert isinstance(board._matrix[4, 4], Cell)
    assert board._matrix[4, 4].shipUUID == ship.uuid
    assert board._matrix[4, 4].squareIndex == 1
    assert board._matrix[4, 4].alive is True

    assert isinstance(board._matrix[5, 4], Cell)
    assert board._matrix[5, 4].shipUUID == ship.uuid
    assert board._matrix[5, 4].squareIndex == 2
    assert board._matrix[5, 4].alive is True

    assert isinstance(board._matrix[6, 4], Cell)
    assert board._matrix[6, 4].shipUUID == ship.uuid
    assert board._matrix[6, 4].squareIndex == 3
    assert board._matrix[6, 4].alive is True

    assert player.ships[ship.uuid].location == (3, 4)
    assert player.ships[ship.uuid].orientation == "RIGHT"


def test_board_add_ship_with_damage():
    # This functionality isn't really
    # crucial but it makes the code more versitale and allows
    # for implementing custom game modes in the future

    ship = Ship(4)
    ship._squares = [True, False, True, True]

    player = Player(ships=[ship])
    board = Board(player=player)

    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")

    assert isinstance(board._matrix[3, 4], Cell)
    assert board._matrix[3, 4].shipUUID == ship.uuid
    assert board._matrix[3, 4].squareIndex == 0
    assert board._matrix[3, 4].alive is True

    assert isinstance(board._matrix[4, 4], Cell)
    assert board._matrix[4, 4].shipUUID == ship.uuid
    assert board._matrix[4, 4].squareIndex == 1
    assert board._matrix[4, 4].alive is False

    assert isinstance(board._matrix[5, 4], Cell)
    assert board._matrix[5, 4].shipUUID == ship.uuid
    assert board._matrix[5, 4].squareIndex == 2
    assert board._matrix[5, 4].alive is True

    assert isinstance(board._matrix[6, 4], Cell)
    assert board._matrix[6, 4].shipUUID == ship.uuid
    assert board._matrix[6, 4].squareIndex == 3
    assert board._matrix[6, 4].alive is True

    assert player.ships[ship.uuid].location == (3, 4)
    assert player.ships[ship.uuid].orientation == "RIGHT"


def test_board_add_ship_cell_already_occupied():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)

    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")

    with pytest.raises(CellAlreadyOccupiedError):
        board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")


def test_board_add_ship_does_not_exist():
    player = Player()
    board = Board(player=player)

    with pytest.raises(ShipDoesNotExistError):
        board.add_ship(shipUUID=10, location=(3, 4), orientation="RIGHT")


def test_board_remove_ship():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)
    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")
    board.remove_ship(shipUUID=ship.uuid)

    assert board._matrix[3, 4] is None
    assert board._matrix[4, 4] is None
    assert board._matrix[5, 4] is None
    assert board._matrix[6, 4] is None


def test_board_remove_ship_does_not_exist():
    player = Player()
    board = Board(player=player)

    with pytest.raises(ShipDoesNotExistError):
        board.remove_ship(shipUUID=11)


def test_board_remove_ship_invalid_data():
    ship = Ship(4)
    ship._location = (456, 1)
    player = Player(ships=[ship])
    board = Board(player=player)

    with pytest.raises(LocationOutsideOfRangeError):
        board.remove_ship(shipUUID=ship.uuid)


def test_board_remove_ship_unlocated():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)

    with pytest.raises(UnlocatedShipRemovalError):
        board.remove_ship(shipUUID=ship.uuid)


def test_board_move_ship():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)
    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")
    board.move_ship(shipUUID=ship.uuid, location=(4, 4), orientation="UP")

    # Check that the ship is in the correct location
    assert isinstance(board._matrix[4, 4], Cell)
    assert board._matrix[4, 4].shipUUID == ship.uuid
    assert board._matrix[4, 4].squareIndex == 0
    assert board._matrix[4, 4].alive is True

    assert isinstance(board._matrix[4, 5], Cell)
    assert board._matrix[4, 5].shipUUID == ship.uuid
    assert board._matrix[4, 5].squareIndex == 1
    assert board._matrix[4, 5].alive is True

    assert isinstance(board._matrix[4, 6], Cell)
    assert board._matrix[4, 6].shipUUID == ship.uuid
    assert board._matrix[4, 6].squareIndex == 2
    assert board._matrix[4, 6].alive is True

    assert isinstance(board._matrix[4, 7], Cell)
    assert board._matrix[4, 7].shipUUID == ship.uuid
    assert board._matrix[4, 7].squareIndex == 3
    assert board._matrix[4, 7].alive is True

    # Old location should be empty
    assert board._matrix[3, 4] is None

    assert player.ships[ship.uuid].location == (4, 4)
    assert player.ships[ship.uuid].orientation == "UP"


def test_board_move_unlocated_ship():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)
    board.move_ship(shipUUID=ship.uuid, location=(4, 4), orientation="UP")

    # It should work like adding the ship
    assert isinstance(board._matrix[4, 4], Cell)
    assert board._matrix[4, 4].shipUUID == ship.uuid
    assert board._matrix[4, 4].squareIndex == 0
    assert board._matrix[4, 4].alive is True

    assert isinstance(board._matrix[4, 5], Cell)
    assert board._matrix[4, 5].shipUUID == ship.uuid
    assert board._matrix[4, 5].squareIndex == 1
    assert board._matrix[4, 5].alive is True

    assert isinstance(board._matrix[4, 6], Cell)
    assert board._matrix[4, 6].shipUUID == ship.uuid
    assert board._matrix[4, 6].squareIndex == 2
    assert board._matrix[4, 6].alive is True

    assert isinstance(board._matrix[4, 7], Cell)
    assert board._matrix[4, 7].shipUUID == ship.uuid
    assert board._matrix[4, 7].squareIndex == 3
    assert board._matrix[4, 7].alive is True

    assert player.ships[ship.uuid].location == (4, 4)
    assert player.ships[ship.uuid].orientation == "UP"


def test_board_get_cell():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)
    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")

    assert board.cell(3, 4) == board._matrix[3, 4]
    assert board.cell(0, 0) == board._matrix[0, 0]


def test_board_get_cell_index_error():
    player = Player()
    board = Board(player=player)

    with pytest.raises(LocationOutsideOfRangeError):
        board.cell(123, 1)


def test_board_get_possible_locations_1():
    player = Player()
    board = Board(player=player)

    assert board.get_possible_locations(size=10, orientation="RIGHT") == [
        (0, i) for i in range(board._size)
    ]


def test_board_get_possible_locations_2():
    player = Player()
    board = Board(player=player)

    assert board.get_possible_locations(size=5, orientation="RIGHT") == [
        (i, j) for i in range(board._size - 5 + 1) for j in range(board._size)
    ]


def test_board_get_possible_locations_occupied_squares_1():
    player = Player()
    board = Board(player=player)
    board._matrix[3, 4] = Cell(shipUUID=1, squareIndex=0, alive=True)
    board._matrix[3, 5] = Cell(shipUUID=1, squareIndex=1, alive=True)
    board._matrix[3, 6] = Cell(shipUUID=1, squareIndex=3, alive=True)

    assert board.get_possible_locations(size=10, orientation="RIGHT") == [
        (0, i) for i in chain(range(3), range(8, board._size))
    ]


def test_board_get_possible_locations_occupied_squares_2():
    player = Player()
    board = Board(player=player)
    board._matrix[0, 0] = Cell(shipUUID=1, squareIndex=0, alive=True)
    board._matrix[1, 0] = Cell(shipUUID=1, squareIndex=1, alive=True)
    board._matrix[2, 0] = Cell(shipUUID=1, squareIndex=3, alive=True)

    assert board.get_possible_locations(size=10, orientation="RIGHT") == [
        (0, i) for i in range(2, board._size)
    ]


def test_board_get_possible_locations_occupied_squares_3():
    player = Player()
    board = Board(player=player)
    board._matrix[0, 0] = Cell(shipUUID=1, squareIndex=0, alive=True)

    assert board.get_possible_locations(size=10, orientation="RIGHT") == [
        (0, i) for i in range(2, board._size)
    ]


def test_board_attack_hit():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)
    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")

    assert board.attack(3, 4) == AttackResult.HIT
    assert ship[0] is False
    assert board._player.fleet_strength == 3


def test_board_attack_miss():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)
    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")

    assert board.attack(3, 3) == AttackResult.MISS


def test_board_attack_sunk():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)
    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")

    assert board.attack(3, 4) == AttackResult.HIT
    assert board.attack(4, 4) == AttackResult.HIT
    assert board.attack(5, 4) == AttackResult.HIT
    assert board.attack(6, 4) == AttackResult.SUNK
    assert ship.strength == 0
    assert board._player.fleet_strength == 0


def test_board_attack_destroyed_cell():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)
    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")
    board.attack(3, 4)

    with pytest.raises(HitDestroyedSquareError):
        board.attack(3, 4)
