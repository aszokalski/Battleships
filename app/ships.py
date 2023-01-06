from utils import get_uuid
from config import (
    BOARD_SIZE,
    DEFAULT_ORIENTATION,
    BOAT_SIZES
)
from typing import Literal


class LocationOutsideOfRangeError(IndexError):
    pass


class IncorrectOrientationError(ValueError):
    pass


class UnlocatedShipHitError(ValueError):
    pass


class HitOutsideOfRangeError(IndexError):
    pass


class HitDestroyedSquareError(IndexError):
    pass


class Ship:
    """Ship base object

    Args:
        size (int): size of the ship
    """
    def __init__(self, size: int) -> None:
        self._squares = [True for i in range(size)]
        self._uuid = get_uuid()
        self._location = None
        self._orientation = DEFAULT_ORIENTATION

    @property
    def squares(self) -> list:
        """List of the ship's 'squares' containing True / False values. (False - destroyed)

        Returns:
            list: squares
        """
        return self._squares

    @property
    def size(self) -> int:
        """Size of the ship - number of its squares

        Returns:
            int: size
        """
        return len(self._squares)

    @property
    def strength(self) -> int:
        """Strength of the ship - number of undestroyed squares

        Returns:
            int: strength
        """
        return sum(self._squares)

    @property
    def uuid(self) -> int:
        """Unique ID

        Returns:
            int: uuid
        """
        return self._uuid

    @property
    def location(self) -> tuple | None:
        """Ship location tuple (x, y). If the location is not set it returns None.

        Returns:
            tuple | None: location

        Raises:
            LocationOutsideOfRangeError: location is not on the board
        """
        return self._location

    @location.setter
    def location(self, value: tuple) -> None:
        if (any(index not in range(0, BOARD_SIZE)
                for index in value)):
            raise LocationOutsideOfRangeError(f"Given location {value} does not fit on a {BOARD_SIZE}x{BOARD_SIZE} matrix")

        self._location = value

    @property
    def orientation(self) -> str:
        """Ship's orientation ("UP", "DOWN", "LEFT","RIGHT").
        Default: "UP"

        Returns:
            str: orientation

        Raises:
            IncorrectOrientationError: Orientation is not "UP", "DOWN", "LEFT", "RIGHT"
        """
        return self._orientation

    @orientation.setter
    def orientation(self, value: Literal["UP", "DOWN", "RIGHT", "LEFT"]) -> None:
        orientations = ["UP", "DOWN", "RIGHT", "LEFT"]
        if (value not in orientations):
            raise IncorrectOrientationError(f"{value} not in {orientations}")

        self._orientation = value

    def take_a_hit(self, targetIndex: int):
        """Destroys a given square

        Args:
            targetIndex (int): index of the square to be destroyed

        Raises:
            UnlocatedShipHitError: if the ship is not located
            HitOutsideOfRangeError: if the targetIndex is not in range
            HitDestroyedSquareError: if the targeted square already is False

        Returns:
            int: strength after the hit (0 is destroyed)
        """
        if (not self.location):
            raise UnlocatedShipHitError("You cannot hit an unlocated ship")
        if (targetIndex >= self.size):
            raise HitOutsideOfRangeError(f"{targetIndex} is not within 0-{self.size-1} range")
        if (not self.squares[targetIndex]):
            raise HitDestroyedSquareError(f"ship: {self._uuid} square: {targetIndex} is already destroyed")
        self.squares[targetIndex] = False
        return self.strength


class Carrier(Ship):
    def __init__(self) -> None:
        super().__init__(BOAT_SIZES['Carrier'])


class Battleship(Ship):
    def __init__(self) -> None:
        super().__init__(BOAT_SIZES['Battleship'])


class Destroyer(Ship):
    def __init__(self) -> None:
        super().__init__(BOAT_SIZES['Destroyer'])


class Submarine(Ship):
    def __init__(self) -> None:
        super().__init__(BOAT_SIZES['Submarine'])


class PatrolBoat(Ship):
    def __init__(self) -> None:
        super().__init__(BOAT_SIZES['PatrolBoat'])