from boards import Board
from ships import get_default_ship_set
from ui import CLI, ShipPlacementAborted
from random import choice
import config


class EnemyUnsetError(Exception):
    pass


class Player:
    def __init__(
        self,
        name: str = "Unnamed",
        ships: list = None,
        side: int = config.DEFAULT_PLAYER_SIDE,
        ui: CLI | None = None,
    ) -> None:
        """Player class

        Args:
            name (str, optional): player's name. Defaults to "Unnamed".
            ships (list, optional): initial ship list. If not set, default ship set will be used. Defaults to None.
            side (int, optional): side to display the board (0 - left, 1 - right)
            ui (CLI | None, optional): CLI object to use. (if not set CLI will not be used) Defaults to None
        """
        ships = ships if ships else get_default_ship_set()
        self._ships = {ship.uuid: ship for ship in ships}
        self._name = name
        self._board = Board(self)
        self._side = side
        self._enemy = None
        self._fleet_strength = sum([ship.size for ship in ships])
        self._ui = ui

    @property
    def ships(self) -> dict:
        """Returns the player's ships

        Returns:
            dict: player's ships
        """
        return self._ships

    @property
    def name(self) -> str:
        """Returns the player's name

        Returns:
            str: player's name
        """
        return self._name

    @property
    def side(self) -> str:
        """Returns the player's side

        Returns:
            int: player's side
        """
        return self._side

    @property
    def board(self) -> Board:
        """Returns the player's board object

        Returns:
            Board: player's board
        """
        return self._board

    @property
    def enemy_board(self) -> Board:
        """Returns the enemy's board object

        Raises:
            EnemyUnsetError: if the enemy is not set

        Returns:
            Board: enemy's board
        """
        if self._enemy is None:
            raise EnemyUnsetError("Enemy board is not set")
        return self._enemy.board

    @property
    def fleet_strength(self) -> int:
        """Returns the player's fleet strength (sum of all ships' sizes)

        Returns:
            int: player's fleet strength
        """
        return self._fleet_strength

    @fleet_strength.setter
    def fleet_strength(self, value: int) -> None:
        self._fleet_strength = value

    def set_enemy(self, enemy: "Player") -> None:
        """Sets the enemy

        Args:
            enemy (Player): enemy player
        """
        self._enemy = enemy

    def initialize_board(self) -> None:
        """Initializes the board according to the user input"""
        i = 0
        while i < len(self.ships):
            ship = list(self.ships.values())[i]
            try:
                ship.under_edition = True
                x, y, orientation = self._ui.get_move_ship_data(ship, self.board)
                self.board.move_ship(ship.uuid, (x, y), orientation)
                i += 1
                ship.under_edition = False
            except ShipPlacementAborted:
                if i > 0:
                    i -= 1


class AIPlayer(Player):
    def __init__(
        self,
        name: str = "AI",
        ships: list = None,
        side: int = config.DEFAULT_PLAYER_SIDE,
    ) -> None:
        """Player that makes smart moves on its own

        Args:
            name (str, optional): player's name. Defaults to "Unnamed".
            ships (list, optional): initial ship list. If not set, default ship set will be used. Defaults to None.
            side (int, optional): side to display the board (0 - left, 1 - right)
        """
        super().__init__(name, ships, side, None)

    def initialize_board(self) -> None:
        """Initializes the board with random ship placement"""
        for ship in self.ships.values():
            orientation = choice(["UP", "DOWN", "LEFT", "RIGHT"])
            x, y = choice(self.board.get_possible_locations(ship.size, orientation))

            self.board.move_ship(ship.uuid, (x, y), orientation)
