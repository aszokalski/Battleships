import config
import numpy as np
from players import Player
from typing import Literal


class DoubleDestructionError(IndexError):
    pass


class InvalidShipPlacementError(IndexError):
    pass


class CellAlreadyOccupiedError(IndexError):
    pass


class Cell:
    def __init__(self, shipUUID: int, squareIndex: int, alive: bool) -> None:
        """Board cell class

        Args:
            shipUUID (int): uuid of the ship that occupies that cell
            squareIndex (int): index of the ship's square
            alive (bool): defines wether the square has not been destroyed yet
        """
        self.shipUUID = shipUUID
        self.squareIndex = squareIndex
        self._alive = alive

    @property
    def alive(self):
        """Defines wether the square has not been destroyed yet"""
        return self._alive

    def destroy(self):
        """Destroys the cell

        Raises:
            DoubleDestructionError: if the cell has already been destroyed
        """
        if (not self.alive):
            raise DoubleDestructionError

        self._alive = False


class Board:
    def __init__(self, player: Player) -> None:
        """Board class

        Args:
            player (Player): player that owns the board
        """
        self._player = player
        self._size = config.BOARD_SIZE
        self._matrix = np.array([None for _ in range(self._size**2)]).reshape(self._size, self._size)

    def _calculate_square_locations(self, start_location: tuple,
                                    orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"], size: int) -> list:
        """Calculates the locations of the squares of a ship

        Args:
            start_location (tuple): location of the first square of the ship
            orientation (Literal["UP", "DOWN", "LEFT", "RIGHT"]): orientation of the ship
            size (int): size of the ship

        Raises:
            InvalidShipPlacementError: if the ship would not fit on the board

        Returns:
            list: list of the locations of the squares of the ship
        """

        orientation_operation = {
            "UP": lambda loc, x: (loc[0], loc[1] + x),
            "DOWN": lambda loc, x: (loc[0], loc[1] - x),
            "LEFT": lambda loc, x: (loc[0] - x, loc[1]),
            "RIGHT": lambda loc, x: (loc[0] + x, loc[1]),
        }

        move = orientation_operation[orientation]
        end_location = move(
            start_location,
            size - 1
        )

        if any(coordinate not in range(self._size)
               for coordinate in end_location):
            raise InvalidShipPlacementError("Ship would not fit on the board")

        return [move(start_location, x) for x in range(size)]

    def add_ship(self, shipUUID: int, location: tuple, orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"]):
        """Adds a ship to the board

        Args:
            shipUUID (int): uuid of the ship to add
            location (tuple): location of the first square of the ship
            orientation (Literal["UP", "DOWN", "LEFT", "RIGHT"]): orientation of the ship

        Raises:
            CellAlreadyOccupiedError: if the ship would overlap with another ship
            InvalidShipPlacementError: if the ship would not fit on the board

        """
        ship = self._player.ships[shipUUID]
        square_locations = self._calculate_square_locations(
            location,
            orientation,
            ship.size
        )

        if any(self._matrix[*square] is not None
               for square in square_locations):
            raise CellAlreadyOccupiedError("Ship would overlap with another ship")

        for index, square in enumerate(square_locations):
            self._matrix[*square] = Cell(
                shipUUID=shipUUID,
                squareIndex=index,
                alive=True
            )
        ship.location = location
        ship.orientation = orientation


class PlayerBoard(Board):
    pass
