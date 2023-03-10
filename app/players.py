from boards import Board
from ships import Ship, get_default_ship_set
from ui import CLI, ActionAborted
from utils import AttackResult
from random import choice
from config import config
import cli_config


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
        self._last_attack_result = None

    @property
    def ships(self) -> dict[int, Ship]:
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
    def last_attack_result(self) -> AttackResult:
        """Returns the last attack result

        Returns:
            AttackResult: last attack result enum
        """
        return self._last_attack_result

    @last_attack_result.setter
    def last_attack_result(self, value: AttackResult) -> None:
        self._last_attack_result = value

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

    def _edit_board(self):
        """Edits the board using the user input.
        First the user selects a ship,
        then the ship is moved to the desired location.

        If the user aborts the ship placement,
        the ship is not moved.

        If the user selects a cell that is not a ship,
        the user is asked to select a ship again."""

        while True:
            try:
                x, y = self._ui.get_location(
                    self.board,
                    instructions=cli_config.instructions["editing"],
                    abortable=True,
                )
            except ActionAborted:
                return
            cell = self.board.cell(x, y)
            if cell is not None:
                break

        ship = self.ships[cell.shipUUID]
        try:
            ship.under_edition = True
            x, y, orientation = self._ui.get_move_ship_data(ship, self.board)
            self.board.move_ship(ship.uuid, (x, y), orientation)
        except ActionAborted:
            pass

        ship.under_edition = False

        self._ui.show_menu(
            "Do you confirm this ship placement?",
            {"Confirm": lambda: None, "Edit": self._edit_board},
            self.board,
        )()

    def initialize_board(self) -> None:
        """Initializes the board using the user input"""
        i = 0
        randomize = False
        while i < len(self.ships) and not randomize:
            ship = list(self.ships.values())[i]
            try:
                ship.under_edition = True
                data = self._ui.get_move_ship_data(ship, self.board, True)
                if data:
                    x, y, orientation = data
                    self.board.move_ship(ship.uuid, (x, y), orientation)
                    i += 1
                else:
                    randomize = True
                ship.under_edition = False
            except ActionAborted:
                if i > 0:
                    i -= 1

        if randomize:
            for ship in self.ships.values():
                orientation = choice(["UP", "DOWN", "LEFT", "RIGHT"])
                x, y = choice(self.board.get_possible_locations(ship.size, orientation))
                self.board.move_ship(ship.uuid, (x, y), orientation)
                ship.under_edition = False

        self._ui.show_menu(
            "Do you confirm this ship placement?",
            {"Confirm": lambda: None, "Edit": self._edit_board},
            self.board,
        )()

    def attack_enemy(self) -> AttackResult:
        """Attacks the enemy using the user input

        Returns:
            AttackResult: result of the attack
        """
        if self._enemy is None:
            raise EnemyUnsetError("Enemy is not set")

        while True:
            x, y = self._ui.get_location(
                self.enemy_board, self.board, True, cli_config.instructions["attacking"]
            )
            if self.enemy_board.cell(x, y) is None or self.enemy_board.cell(x, y).alive:
                self.last_attack_result = self.enemy_board.attack(x, y)
                break


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
        self._target_list = []
        self._previous_hit = None
        self._previous_shots = []
        super().__init__(name, ships, side, None)

    def set_enemy(self, enemy: "Player") -> None:
        return super().set_enemy(enemy)

    def initialize_board(self) -> None:
        """Initializes the board with random ship placement"""
        for ship in self.ships.values():
            orientation = choice(["UP", "DOWN", "LEFT", "RIGHT"])
            x, y = choice(self.board.get_possible_locations(ship.size, orientation))
            self.board.move_ship(ship.uuid, (x, y), orientation)
            ship.under_edition = False

    def attack_enemy(self) -> AttackResult:
        """Attacks the enemy using the hunt-target strategy.
        Hunt mode: hitting random cells. If the last attack was a hit, the algorithm switches to target mode.
        Target mode: hitting cells around the last hit cell. If the ship is sunk, the algorithm switches to hunt mode.

        Returns:
            AttackResult: result of the attack
        """
        if self._enemy is None:
            raise EnemyUnsetError("Enemy is not set")
        while True:
            if len(self._target_list) > 0:
                x, y = self._target_list.pop()
            else:
                possible_locations = []
                for i in range(config.BOARD_SIZE):
                    for j in range(config.BOARD_SIZE):
                        if (i, j) not in self._previous_shots:
                            possible_locations.append((i, j))
                x, y = x, y = choice(possible_locations)

            if self.enemy_board.cell(x, y) is None or self.enemy_board.cell(x, y).alive:
                self._previous_shots.append((x, y))
                self.last_attack_result = self.enemy_board.attack(x, y)
                if self.last_attack_result == AttackResult.HIT:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (
                                x + i in range(config.BOARD_SIZE)
                                and y + j in range(config.BOARD_SIZE)
                                and (x + i, y + j) not in self._target_list
                            ):

                                self._target_list.append((x + i, y + j))

                    new_target_list = []
                    for target in self._target_list:
                        if target == self._previous_hit or target == (x, y):
                            pass
                        elif (target[0] == x or target[1] == y) and (
                            self._previous_hit is None
                            or target[0] == self._previous_hit[0]
                            or target[1] == self._previous_hit[1]
                        ):
                            new_target_list.append(target)
                    self._target_list = new_target_list
                    self._previous_hit = (x, y)
                elif self.last_attack_result == AttackResult.SUNK:
                    self._target_list = []
                    self._previous_hit = None

                break
