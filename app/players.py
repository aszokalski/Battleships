from boards import Board
from ships import get_default_ship_set


class EnemyUnsetError(Exception):
    pass


class Player:
    def __init__(self, name: str = "Unnamed", ships: list = None) -> None:
        ships = ships if ships else get_default_ship_set()
        self._ships = {ship.uuid: ship for ship in ships}
        self._name = name
        self._board = Board(self)
        self._enemy = None
        self._fleet_strength = sum([ship.size for ship in ships])

    @property
    def ships(self) -> dict:
        return self._ships

    @property
    def name(self) -> str:
        return self._name

    @property
    def board(self) -> Board:
        return self._board

    @property
    def enemy_board(self) -> Board:
        if self._enemy is None:
            raise EnemyUnsetError("Enemy board is not set")
        return self._enemy.board

    @property
    def fleet_strength(self) -> int:
        return self._fleet_strength

    @fleet_strength.setter
    def fleet_strength(self, value: int) -> None:
        self._fleet_strength = value

    def set_enemy(self, enemy) -> None:
        self._enemy = enemy


class AIPlayer(Player):
    pass
