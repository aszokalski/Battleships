from boards import (
    Board,
    Cell,
    DoubleDestructionError,
    InvalidShipPlacementError,
    CellAlreadyOccupiedError
)
from players import (
    Player
)
from ships import (
    Ship
)
import config
import pytest
import numpy as np


def test_cell_constructor():
    cell = Cell(
        shipUUID=57,
        squareIndex=2,
        alive=True
    )

    assert cell.shipUUID == 57
    assert cell.squareIndex == 2
    assert cell._alive is True


def test_cell_destroy():
    cell = Cell(
        shipUUID=57,
        squareIndex=2,
        alive=True
    )

    cell.destroy()
    assert cell.alive is False


def test_cell_destroy_dead():
    cell = Cell(
        shipUUID=57,
        squareIndex=2,
        alive=False
    )
    with pytest.raises(DoubleDestructionError):
        cell.destroy()


def test_board_constructor():
    player = Player()
    board = Board(
        player=player
    )
    board_size = config.BOARD_SIZE
    empty_matrix = np.array([None for _ in range(board_size**2)]).reshape(board_size, board_size)

    assert board._player == player
    assert board._size == board_size
    assert np.array_equal(board._matrix, empty_matrix)


def test_board_calculate_square_locations_UP():
    player = Player()
    board = Board(
        player=player
    )
    assert board._calculate_square_locations(
        start_location=(0, 0),
        orientation="UP",
        size=5
    ) == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]


def test_board_calculate_square_locations_DOWN():
    player = Player()
    board = Board(
        player=player
    )
    assert board._calculate_square_locations(
        start_location=(0, 4),
        orientation="DOWN",
        size=5
    ) == [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]


def test_board_calculate_square_locations_RIGHT():
    player = Player()
    board = Board(
        player=player
    )
    assert board._calculate_square_locations(
        start_location=(0, 0),
        orientation="RIGHT",
        size=5
    ) == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]


def test_board_calculate_square_locations_LEFT():
    player = Player()
    board = Board(
        player=player
    )
    assert board._calculate_square_locations(
        start_location=(4, 0),
        orientation="LEFT",
        size=5
    ) == [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]


def test_board_calculate_square_locations_sticking_out_1():
    player = Player()
    board = Board(
        player=player
    )
    with pytest.raises(InvalidShipPlacementError):
        board._calculate_square_locations(
            start_location=(3, 0),
            orientation="LEFT",
            size=5
        )


def test_board_calculate_square_locations_sticking_out_2():
    player = Player()
    board = Board(
        player=player
    )
    with pytest.raises(InvalidShipPlacementError):
        board._calculate_square_locations(
            start_location=(7, 0),
            orientation="RIGHT",
            size=5
        )


def test_board_add_ship():
    player = Player()
    ship = Ship(4)
    board = Board(
        player=player
    )

    board.add_ship(
        shipUUID=ship.uuid,
        location=(3, 4),
        orientation="RIGHT"
    )

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
    board = Board(
        player=player
    )

    board.add_ship(
        shipUUID=ship.uuid,
        location=(3, 4),
        orientation="RIGHT"
    )

    with pytest.raises(CellAlreadyOccupiedError):
        board.add_ship(
            shipUUID=ship.uuid,
            location=(3, 4),
            orientation="RIGHT"
        )
