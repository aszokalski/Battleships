from boards import Board
from ships import get_default_ship_set


class Player:
    def __init__(self, name: str = "Unnamed", ships: list = None) -> None:
        ships = ships if ships else get_default_ship_set()
        self._ships = {ship.uuid: ship for ship in ships}
        self._name = name
        self._board = Board(self)

    @property
    def ships(self):
        return self._ships

    @property
    def name(self):
        return self._name


class AIPlayer(Player):
    pass
