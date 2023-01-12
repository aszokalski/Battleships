import config
import numpy as np
from players import Player
from typing import Literal
from ships import Ship, LocationOutsideOfRangeError
from utils import AttackResult


class DoubleDestructionError(IndexError):
    pass


class CellAlreadyOccupiedError(IndexError):
    pass


class ShipDoesNotExistError(KeyError):
    pass


class UnlocatedShipRemovalError(IndexError):
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
        if not self.alive:
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
        self._matrix = np.array([None for _ in range(self._size**2)]).reshape(
            self._size, self._size
        )

    def _calculate_square_locations(
        self,
        start_location: tuple,
        orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"],
        size: int,
    ) -> list:
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
        end_location = move(start_location, size - 1)

        if any(coordinate not in range(self._size) for coordinate in end_location):
            raise LocationOutsideOfRangeError("Ship would not fit on the board")

        return [move(start_location, x) for x in range(size)]

    def _get_ship_object(self, shipUUID: int) -> Ship:
        """Returns the ship object associated with the given uuid

        Args:
            shipUUID (int): uuid of the ship

        Raises:
            ShipDoesNotExistError: if the ship does not exist

        Returns:
            Ship: ship object
        """
        try:
            return self._player.ships[shipUUID]
        except KeyError:
            raise ShipDoesNotExistError("Ship does not exist")

    def add_ship(
        self,
        shipUUID: int,
        location: tuple,
        orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"],
    ) -> None:
        """Adds a ship to the board

        Args:
            shipUUID (int): uuid of the ship to add
            location (tuple): location of the first square of the ship
            orientation (Literal["UP", "DOWN", "LEFT", "RIGHT"]): orientation of the ship

        Raises:
            CellAlreadyOccupiedError: if the ship would overlap with another ship
            InvalidShipPlacementError: if the ship would not fit on the board
            ShipDoesNotExistError: if the ship does not exist

        """
        ship = self._get_ship_object(shipUUID)
        square_locations = self._calculate_square_locations(
            location, orientation, ship.size
        )

        if any(self._matrix[*square] is not None for square in square_locations):
            raise CellAlreadyOccupiedError("Ship would overlap with another ship")

        for index, square in enumerate(square_locations):
            self._matrix[*square] = Cell(
                shipUUID=shipUUID, squareIndex=index, alive=True
            )
        ship.location = location
        ship.orientation = orientation

    def remove_ship(self, shipUUID: int) -> None:
        """Removes a ship from the board

        Args:
            shipUUID (int): uuid of the ship to remove

        Raises:
            InvalidShipPlacementError: given ship is incorrectly placed
            ShipDoesNotExistError: if the ship does not exist
            UnlocatedShipRemovalError: if the ship is not located
        """
        ship = self._get_ship_object(shipUUID)
        if not ship.location:
            raise UnlocatedShipRemovalError("Ship is not located")

        square_locations = self._calculate_square_locations(
            ship.location, ship.orientation, ship.size
        )

        for location in square_locations:
            self._matrix[*location] = None
        ship.location = None

    def move_ship(
        self,
        shipUUID: int,
        location: tuple,
        orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"],
    ) -> None:
        """Moves a ship to a new location. If the ship is not located it works like ``self.add_ship``

        Args:
            shipUUID (int): uuid of the ship to move
            location (tuple): new location of the ship

        Raises:
            CellAlreadyOccupiedError: if the ship would overlap with another ship
            InvalidShipPlacementError: if the ship location is not valid (it doesn't fit on the board)
            ShipDoesNotExistError: if the ship does not exist
        """
        try:
            self.remove_ship(shipUUID)
        except UnlocatedShipRemovalError:
            pass
        self.add_ship(shipUUID, location, orientation)

    def cell(self, x: int, y: int) -> Cell | None:
        """Returns the cell at the given coordinates. If there is no cell it returns ``None``

        Args:
            x (int): coordinate x
            y (int): coordinate y

        Raises:
            IndexError: if the coordinates are out of range

        Returns:
            Cell | None: value at the given coordinates
        """
        if any(val not in range(self._size) for val in (x, y)):
            raise LocationOutsideOfRangeError("Index out of range")

        return self._matrix[x, y]

    def get_possible_locations(
        self, size: int, orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"]
    ) -> list:
        """Returns a list of possible locations for a ship of the given size and orientation

        Args:
            size (int): size of the ship
            orientation (Literal["UP", "DOWN", "LEFT", "RIGHT"]): orientation of the ship

        Returns:
            list: list of (x, y) tuples
        """
        location_range_function = {
            "UP": lambda board_size, ship_size: (
                range(board_size),
                range(board_size - ship_size + 1),
            ),
            "DOWN": lambda board_size, ship_size: (
                range(board_size),
                range(ship_size - 1, board_size),
            ),
            "LEFT": lambda board_size, ship_size: location_range_function["DOWN"](
                board_size, ship_size
            )[::-1],
            "RIGHT": lambda board_size, ship_size: location_range_function["UP"](
                board_size, ship_size
            )[::-1],
        }

        x_range, y_range = location_range_function[orientation](self._size, size)

        possible_locations = []
        for x in x_range:
            for y in y_range:
                square_locations = self._calculate_square_locations(
                    (x, y), orientation, size
                )
                if all(self._matrix[*square] is None for square in square_locations):
                    possible_locations.append((x, y))

        return possible_locations

    def attack(self, x: int, y: int) -> AttackResult:
        """Attacks the given location and returns ``AttackResult``

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Raises:
            HitDestroyedSquareError: if the cell has already been hit
            LocationOutsideOfRangeError: if the coordinates are not on the board

        Returns:
            AttackResult: result of the attack
        """
        cell = self.cell(x, y)
        if cell is None:
            return AttackResult.MISS

        ship = self._get_ship_object(cell.shipUUID)
        strength_after_hit = ship.take_a_hit(cell.squareIndex)
        cell.destroy()

        if strength_after_hit == 0:
            return AttackResult.SUNK
        else:
            return AttackResult.HIT


class PlayerBoard(Board):
    pass
