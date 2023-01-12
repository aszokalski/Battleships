from boards import (
    Board,
    Cell,
    DoubleDestructionError,
    InvalidShipPlacementError,
    CellAlreadyOccupiedError,
    ShipDoesNotExistError,
    UnlocatedShipRemovalError,
)
from players import Player
from ships import Ship
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


def test_board_calculate_square_locations_UP():
    player = Player()
    board = Board(player=player)

    assert board._calculate_square_locations(
        start_location=(0, 0), orientation="UP", size=5
    ) == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]


def test_board_calculate_square_locations_DOWN():
    player = Player()
    board = Board(player=player)

    assert board._calculate_square_locations(
        start_location=(0, 4), orientation="DOWN", size=5
    ) == [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]


def test_board_calculate_square_locations_RIGHT():
    player = Player()
    board = Board(player=player)

    assert board._calculate_square_locations(
        start_location=(0, 0), orientation="RIGHT", size=5
    ) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]


def test_board_calculate_square_locations_LEFT():
    player = Player()
    board = Board(player=player)

    assert board._calculate_square_locations(
        start_location=(4, 0), orientation="LEFT", size=5
    ) == [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]


def test_board_calculate_square_locations_sticking_out_1():
    player = Player()
    board = Board(player=player)

    with pytest.raises(InvalidShipPlacementError):
        board._calculate_square_locations(
            start_location=(3, 0), orientation="LEFT", size=5
        )


def test_board_calculate_square_locations_sticking_out_2():
    player = Player()
    board = Board(player=player)

    with pytest.raises(InvalidShipPlacementError):
        board._calculate_square_locations(
            start_location=(7, 0), orientation="RIGHT", size=5
        )


def test_board_add_ship():
    player = Player()
    ship = Ship(4)
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


def test_board_add_ship_cell_already_occupied():
    player = Player()
    ship = Ship(4)
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
    player = Player()
    ship = Ship(4)
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
        board.remove_ship(shipUUID=10)


def test_board_remove_ship_invalid_data():
    ship = Ship(4)
    ship.location = (456, 1)
    player = Player(ships=[ship])
    board = Board(player=player)

    with pytest.raises(InvalidShipPlacementError):
        board.remove_ship(shipUUID=ship.uuid)


def test_board_remove_ship_unlocated():
    ship = Ship(4)
    player = Player(ships=[ship])
    board = Board(player=player)

    with pytest.raises(UnlocatedShipRemovalError):
        board.remove_ship(shipUUID=ship.uuid)


def test_board_move_ship():
    player = Player()
    ship = Ship(4)
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
    player = Player()
    ship = Ship(4)
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
    player = Player()
    ship = Ship(4)
    board = Board(player=player)
    board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")

    assert board.cell(3, 4) == board._matrix[3, 4]
    assert board.cell(0, 0) == board._matrix[0, 0]


def test_board_get_cell_index_error():
    player = Player()
    board = Board(player=player)

    with pytest.raises(IndexError):
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
        (0, i) for i in chain(range(4), range(7, board._size))
    ]


def test_board_get_possible_locations_occupied_squares_2():
    player = Player()
    board = Board(player=player)
    board._matrix[0, 0] = Cell(shipUUID=1, squareIndex=0, alive=True)
    board._matrix[1, 0] = Cell(shipUUID=1, squareIndex=1, alive=True)
    board._matrix[2, 0] = Cell(shipUUID=1, squareIndex=3, alive=True)

    assert board.get_possible_locations(size=10, orientation="RIGHT") == [
        (0, i) for i in range(1, board._size)
    ]


def test_board_get_possible_locations_occupied_squares_3():
    player = Player()
    board = Board(player=player)
    board._matrix[0, 0] = Cell(shipUUID=1, squareIndex=0, alive=True)

    assert board.get_possible_locations(size=10, orientation="RIGHT") == [
        (0, i) for i in range(1, board._size)
    ]
