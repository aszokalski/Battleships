from boards import Board
from ships import Ship
import config
import cli_config
from typing import Callable, Literal
import curses
from enum import IntEnum
from copy import copy
from utils import AttackResult


class ActionAborted(Exception):
    pass


class Styles(IntEnum):
    """Text styles for the CLI

    Args:
        IntEnum: color number
    """

    GRID = 1
    SHIP = 2
    DESTROYED = 3
    SELECTOR = 4
    ERROR = 5
    SUNK = 6


class CLI:
    def __init__(self) -> None:
        """CLI class"""
        self.screen = curses.initscr()

        # Curses settings
        self.screen.keypad(True)
        curses.curs_set(0)
        curses.start_color()
        curses.cbreak()
        curses.echo()

        # Colors
        curses.init_pair(Styles.GRID, *cli_config.colors["grid"])
        curses.init_pair(Styles.SHIP, *cli_config.colors["ship"])
        curses.init_pair(Styles.DESTROYED, *cli_config.colors["destroyed"])
        curses.init_pair(Styles.SELECTOR, *cli_config.colors["selector"])
        curses.init_pair(Styles.ERROR, *cli_config.colors["error"])

    def _calculate_edge_indexes(
        self,
        current_orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"],
        board_size: int,
        ship_size: int,
    ) -> tuple:
        """A helper function to calculate the edge positions of the ship on the board

        Args:
            current_orientation (Literal["UP", "DOWN", "LEFT", "RIGHT"]): current orientation of the ship
            board_size (int): board size
            ship_size (int): ship size

        Returns:
            tuple: (max_x, min_x, max_y, min_y)
        """
        max_y = (
            board_size - ship_size if current_orientation == "UP" else board_size - 1
        )
        min_y = ship_size - 1 if current_orientation == "DOWN" else 0
        min_x = ship_size - 1 if current_orientation == "LEFT" else 0
        max_x = (
            board_size - ship_size if current_orientation == "RIGHT" else board_size - 1
        )
        return (max_x, min_x, max_y, min_y)

    def _show_remaining_fleet(self, board: Board) -> None:
        """Shows the remaining fleet during positioning

        Args:
            board (Board): board on which the positioning occurs
        """
        horizontal_offset = (
            config.BOARD_SIZE + config.DEFAULT_SPACE_BETWEEN_BOARDS + 1
            if board.player.side == 0
            else 1
        )

        self.screen.addstr(0, horizontal_offset * 2, "Remaining fleet:")

        tab_width = 3
        ship_type_groups = {}
        for ship in board.player.ships.values():
            if ship.under_edition is True:
                ship_type = str(ship)
                group = ship_type_groups.get(ship_type, [])
                group.append(ship)
                ship_type_groups[ship_type] = group

        for i, (ship_type, ships) in enumerate(ship_type_groups.items()):
            self.screen.addstr(
                2 + i,
                horizontal_offset * 2,
                f"{len(ships):>{tab_width+1}}x {ship_type:<10} ({ships[0].size})",
                curses.A_BOLD if i == 0 else 0,
            )

    def _draw_ship(
        self,
        ship: Ship,
        board: Board,
        ship_square_locations: list,
        possible_location: bool = True,
    ) -> None:
        """Draws a ship on the board. It clolors the ship ``cli_config.colors["error"]``
        if it's not possible to place it there.

        Args:
            ship (Ship): ship object
            board (Board): board object
            ship_square_locations (list): list of (x, y) locations of the ship
            possible_location (bool, optional): indicates if it's possible to place
            the ship in that location. Defaults to True.
        """
        horizontal_offset = (
            config.BOARD_SIZE + config.DEFAULT_SPACE_BETWEEN_BOARDS + 1
            if board.player.side == 1
            else 1
        )

        for i, location in enumerate(ship_square_locations):
            draw_y = board.size - location[1] + 1
            draw_x = 2 * (horizontal_offset + location[0])

            alive = ship[i]
            color = Styles.SHIP if possible_location else Styles.ERROR
            self.screen.addstr(
                draw_y,
                draw_x,
                cli_config.symbols["ship"] if alive else cli_config.symbols["shipHit"],
                curses.color_pair(color) | (curses.A_BOLD if i == 0 else 0),
            )

    def _next_orientation(
        self,
        current_orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"],
        location: tuple,
        board_size: int,
        ship_size: int,
    ) -> Literal["UP", "DOWN", "LEFT", "RIGHT"]:
        """Calculates the next (clockwise) orientation of the ship.
        If it is not possible to rotate the ship in a given location,
        it returns the current orientation.

        Returns:
            Literal["UP", "DOWN", "LEFT", "RIGHT"]: Ship orientation
        """
        orientation_cycle = ["UP", "RIGHT", "DOWN", "LEFT"]
        next_orientation = orientation_cycle[
            (orientation_cycle.index(current_orientation) + 1) % 4
        ]

        max_x, min_x, max_y, min_y = self._calculate_edge_indexes(
            next_orientation, board_size, ship_size
        )
        if location[0] in range(min_x, max_x + 1) and location[1] in range(
            min_y, max_y + 1
        ):
            return next_orientation

        return current_orientation

    def _transform_location(
        self, key: int, location: tuple, max_x: int, min_x: int, max_y: int, min_y: int
    ) -> tuple:
        """Transforms a given location based on the user input (key) and given boundaries.

        Args:
            key (int): user input key code
            location (tuple): (x, y)
            max_x (int): max x index
            min_x (int): min x index
            max_y (int): max y index
            min_y (int): min y index

        Returns:
            tuple: (x, y) location
        """
        x, y = location
        if key == curses.KEY_UP and y < max_y:
            y += 1
        elif key == curses.KEY_DOWN and y > min_y:
            y -= 1
        elif key == curses.KEY_LEFT and x > min_x:
            x -= 1
        elif key == curses.KEY_RIGHT and x < max_x:
            x += 1

        return x, y

    def input(self, prompt: str) -> str:
        """Reads user input.

        Args:
            prompt (str): prompt to be shown

        Returns:
            str: user input
        """
        self.screen.clear()
        curses.curs_set(1)
        self.screen.addstr(prompt)
        value = self.screen.getstr()
        curses.curs_set(0)
        return value.decode("utf-8")

    def show_board(
        self,
        board: Board,
        hilight: None | tuple = None,
        ommit_locations: list | None = None,
        skip_refresh: bool = False,
        show_hits_only: bool = False,
        display_strength: bool = False,
    ) -> None:
        """Prints board to the console.

        Args:
            board (Board): The board to be printed
            hilight (None | tuple, optional): (x, y) location to be highlited. Defaults to None.
            ommit_locations (list | None, optional): list of (x, y) locations not to be shown. Defaults to None.
            skip_refresh (bool, optional): Decides of the function will skip the screen refresh. Defaults to False.
            show_hits_only (bool, optional): Decides if only hits will be shown. Defaults to False.
            display_strength (bool, optional): Decides if the ships strength will be shown. Defaults to False.
        """
        horizontal_offset = (
            config.BOARD_SIZE + config.DEFAULT_SPACE_BETWEEN_BOARDS + 1
            if board.player.side == 1
            else 1
        )

        if not skip_refresh:
            self.screen.clear()

        if display_strength:
            header = f"{board.player.name} ({board.player.fleet_strength})"
        else:
            header = board.player.name
        self.screen.addstr(0, (horizontal_offset - 1) * 2, header)

        for i in range(board.size):
            for j in range(board.size):
                cell = board.cell(i, j)
                color = Styles.GRID
                if ommit_locations and (i, j) in ommit_locations or not cell:
                    bold = False
                    symbol = cli_config.symbols["cell"]
                else:
                    sunk = board.player.ships[cell.shipUUID].strength == 0
                    bold = True
                    if cell.alive:
                        color = Styles.SHIP if not show_hits_only else Styles.GRID
                        symbol = (
                            cli_config.symbols["ship"]
                            if not show_hits_only
                            else cli_config.symbols["cell"]
                        )
                    else:
                        if sunk:
                            color = Styles.SUNK
                        else:
                            color = Styles.DESTROYED
                        symbol = cli_config.symbols["shipHit"]
                if hilight and (i, j) == hilight:
                    color = Styles.SELECTOR

                self.screen.addstr(
                    board.size - j + 1,
                    (horizontal_offset + i) * 2,
                    symbol,
                    curses.color_pair(color)
                    | (curses.A_BOLD if bold else curses.A_NORMAL),
                )

        if not skip_refresh:
            self.screen.refresh()

    def get_location(
        self,
        board: Board,
        additional_board: Board | None = None,
        show_hits_only: bool = False,
        instructions: dict | None = None,
        abortable: bool = False,
    ) -> tuple:
        """Gets a location from the user

        Args:
            board (Board): board to get the location from
            additional_board (Board, optional): board to be shown but not to be interacted with. Defaults to None
            show_hits_only (bool, optional): Decides if only hits will be shown on the ``board``. Defaults to False.
            instructions (dict | None, optional): Instructions from ``cli_config.instructions`` to be shown to the user. Defaults to None.
            abortable (bool, optional): Decides if the user can abort the action. Defaults to False.
        Returns:
            tuple: (x, y) location
        Raises:
            ActionAborted: If the user aborts the action
        """
        x, y = 0, 0

        while True:
            self.screen.clear()
            if additional_board:
                self.show_board(
                    board,
                    (x, y),
                    skip_refresh=True,
                    show_hits_only=show_hits_only,
                    display_strength=True,
                )
                self.show_board(
                    additional_board, skip_refresh=True, display_strength=True
                )
                self.screen.refresh()
            else:
                self.show_board(board, (x, y))

            if instructions:
                instructions = copy(instructions)
                if additional_board:
                    enemy_last_result = (
                        additional_board.player._enemy.last_attack_result
                    )
                    if enemy_last_result is not None:
                        if enemy_last_result == AttackResult.HIT:
                            last_attack_str = "HIT your ship"
                        elif enemy_last_result == AttackResult.MISS:
                            last_attack_str = "MISSED"
                        elif enemy_last_result == AttackResult.SUNK:
                            last_attack_str = "SUNK your ship"
                        instructions[
                            "title"
                        ] = f"{additional_board.player._enemy.name} {last_attack_str}!"
                self.show_instructions(instructions)

            key = self.screen.getch()
            if key == ord("\n"):
                break
            elif key in (127, 8) and abortable:  # 127 for darwin and 8 for win
                raise ActionAborted
            else:
                x, y = self._transform_location(
                    key, (x, y), board.size - 1, 0, board.size - 1, 0
                )

        return (x, y)

    def show_instructions(self, data: dict) -> None:
        """Shows given instructions on the screen

        Args:
            data (dict): data from ``cli_config.instructions`` to be shown
        """
        self.screen.addstr(config.BOARD_SIZE + 3, 0, data["title"], curses.A_BOLD)
        self.screen.addstr(config.BOARD_SIZE + 4, 0, data["instructions"])

    def show_menu(
        self, title: str, options: dict[str, any], board: Board | None = None
    ) -> any:
        """Shows a menu on the screen

        Args:
            title (str): title of the menu
            options (dict[str, any]): option_name -> value dictionary
            board (Board | None, optional): Board to show. Defaults to None.

        Returns:
            any: value of the selected option
        """
        option_number = 0
        while True:
            self.screen.clear()
            self.screen.addstr(
                (config.BOARD_SIZE + 3) if board else 0, 0, title, curses.A_BOLD
            )
            if board:
                self.show_board(board, skip_refresh=True)

            tab_width = 3
            for i, option_name in enumerate(options.keys()):
                self.screen.addstr(
                    (config.BOARD_SIZE + 3 if board else 0) + 1 + i,
                    tab_width,
                    option_name,
                    curses.color_pair(Styles.SELECTOR) if option_number == i else 0,
                )

            key = self.screen.getch()
            if key == curses.KEY_DOWN:
                option_number += 1
            elif key == curses.KEY_UP:
                option_number -= 1
            elif key == ord("\n"):
                return list(options.values())[option_number]

            option_number %= 2
            self.screen.refresh()

    def get_move_ship_data(
        self, ship: Ship, board: Board, randomizable: bool = False
    ) -> tuple | None:
        """Gets the new position and orientation of a ship from user.
        It ensures validity of the data.

        Args:
            ship (Ship): ship to move
            board (Board): board to move the ship on
            randomizable(bool, Optional): Decides if the user can randomize the ship placement. Defaults to False.

        Returns:
            tuple | None: (x, y, orientation). If None, the user decided to randomize the ship placement

        Raises:
            ActionAborted: if the user aborts the ship placement
        """

        location = ship.location
        orientation = ship.orientation
        size = ship.size

        x, y = 0, 0

        ommit_locations = []
        if location:
            ommit_locations = board.calculate_square_locations(
                location, orientation, ship.size
            )[0]
            x, y = location

        while True:
            self.screen.clear()
            self.show_board(board, skip_refresh=True, ommit_locations=ommit_locations)
            self._show_remaining_fleet(board)
            self.show_instructions(
                cli_config.instructions[
                    "positioning_random" if randomizable else "positioning"
                ]
            )

            square_locations = board.calculate_square_locations(
                (x, y), orientation, size
            )

            # Check if the ship can be placed there
            if any(
                board.cell(*square) is not None and square not in ommit_locations
                for square in square_locations[1]
            ):
                possible_location = False
            else:
                possible_location = True

            self._draw_ship(ship, board, square_locations[0], possible_location)

            # Read user input
            key = self.screen.getch()

            max_x, min_x, max_y, min_y = self._calculate_edge_indexes(
                orientation, board.size, ship.size
            )
            if key == ord(" "):
                orientation = self._next_orientation(
                    orientation, (x, y), board.size, ship.size
                )
            elif key == ord("\n"):
                if possible_location:
                    return x, y, orientation
            elif key in (127, 8):  # 127 for darwin and 8 for win
                raise ActionAborted
            elif key == ord("r") and randomizable:
                return None
            else:
                x, y = self._transform_location(key, (x, y), max_x, min_x, max_y, min_y)

            self.screen.refresh()

    def wrap(self, function: Callable):
        """Wraps a function to catch keyboard interrupts or other errors and close the screen

        Args:
            function (Callable): function to wrap
        """

        def wrapped_function():
            try:
                return function()
            except KeyboardInterrupt:
                self.close()
            except curses.error:
                self.close()
                print("Terminal window too small. Please resize it and try again.")
            except BaseException as e:
                self.close()
                raise e

        return wrapped_function

    def close(self):
        """Closes the screen"""
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
