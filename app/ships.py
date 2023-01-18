from utils import get_uuid
import config
from typing import Literal
from collections.abc import Sequence


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


class Ship(Sequence):
    """Ship base object

    Args:
        size (int): size of the ship
    """

    def __init__(self, size: int) -> None:
        self._squares = [True for _ in range(size)]
        self._uuid = get_uuid()
        self._location = None
        self._orientation = config.DEFAULT_ORIENTATION
        self._under_edition = True
        super().__init__()

    def __getitem__(self, i):
        """Returns the ship's square at index ``i``"""
        return self._squares[i]

    def __len__(self):
        """Returns the ship's size"""
        return self.size

    @property
    def squares(self) -> list:
        """List of the ship's 'squares' containing ``True`` / ``False`` values. (``False`` - destroyed)

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
        """Ship's unique identifier - used to identify it on the board

        Returns:
            int: uuid
        """
        return self._uuid

    @property
    def location(self) -> tuple | None:
        """Ship location tuple ``(x: int, y: int)``. If the location is not set it returns ``None``.

        Returns:
            tuple | None: location

        Raises:
            LocationOutsideOfRangeError: location is not on the board
        """
        return self._location

    @location.setter
    def location(self, value: tuple) -> None:
        if value is not None and any(
            index not in range(0, config.BOARD_SIZE) for index in value
        ):
            raise LocationOutsideOfRangeError(
                f"Given location {value} does not fit on a {config.BOARD_SIZE}x{config.BOARD_SIZE} matrix"
            )

        self._location = value

    @property
    def orientation(self) -> str:
        """
        Ship's orientation ``"UP", "DOWN", "LEFT","RIGHT"``

        Default: ``"UP"``

        Returns:
            str: orientation

        Raises:
            IncorrectOrientationError: Orientation is not ``"UP", "DOWN", "LEFT", "RIGHT"``
        """
        return self._orientation

    @orientation.setter
    def orientation(self, value: Literal["UP", "DOWN", "RIGHT", "LEFT"]) -> None:
        orientations = ["UP", "DOWN", "RIGHT", "LEFT"]
        if value not in orientations:
            raise IncorrectOrientationError(f"{value} not in {orientations}")

        self._orientation = value

    @property
    def under_edition(self):
        return self._under_edition

    @under_edition.setter
    def under_edition(self, value: bool):
        if type(value) is not bool:
            raise TypeError("under_edition must be a bool")
        self._under_edition = value

    def take_a_hit(self, targetIndex: int):
        """Destroys a given square

        Args:
            targetIndex (int): index of the square to be destroyed

        Raises:
            UnlocatedShipHitError: if the ship is not located
            HitOutsideOfRangeError: if the targetIndex is not in range
            HitDestroyedSquareError: if the targeted square already is ``False``

        Returns:
            int: strength after the hit (``0`` is destroyed)
        """
        if not self.location:
            raise UnlocatedShipHitError("You cannot hit an unlocated ship")
        if targetIndex >= self.size:
            raise HitOutsideOfRangeError(
                f"{targetIndex} is not within 0-{self.size-1} range"
            )
        if not self.squares[targetIndex]:
            raise HitDestroyedSquareError(
                f"ship: {self._uuid} square: {targetIndex} is already destroyed"
            )
        self.squares[targetIndex] = False
        return self.strength


class Carrier(Ship):
    """Ship with ``self.size = BOAT_SIZES['Carrier']`` (Default: ``5``)"""

    def __init__(self) -> None:
        super().__init__(config.BOAT_SIZES["Carrier"])


class Battleship(Ship):
    """Ship with ``self.size = BOAT_SIZES['Battleship']`` (Default: ``4``)"""

    def __init__(self) -> None:
        super().__init__(config.BOAT_SIZES["Battleship"])


class Destroyer(Ship):
    """Ship with ``self.size = BOAT_SIZES['Destroyer']`` (Default: ``3``)"""

    def __init__(self) -> None:
        super().__init__(config.BOAT_SIZES["Destroyer"])


class Submarine(Ship):
    """Ship with ``self.size = BOAT_SIZES['Submarine']`` (Default: ``3``)"""

    def __init__(self) -> None:
        super().__init__(config.BOAT_SIZES["Submarine"])


class PatrolBoat(Ship):
    """Ship with self.size = ``BOAT_SIZES['PatrolBoat']`` (Default: ``2``)"""

    def __init__(self) -> None:
        super().__init__(config.BOAT_SIZES["PatrolBoat"])


def get_default_ship_set():
    ship_name_to_class = {
        "Carrier": Carrier,
        "Battleship": Battleship,
        "Destroyer": Destroyer,
        "Submarine": Submarine,
        "PatrolBoat": PatrolBoat,
    }

    default_ship_set = []
    for qty, name in config.DEFAULT_SHIP_SET:
        for _ in range(qty):
            default_ship_set.append(ship_name_to_class[name]())

    return default_ship_set
