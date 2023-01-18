from boards import Board
from ships import Ship
import config
from typing import Callable, Literal
import curses
from enum import IntEnum


class Styles(IntEnum):
    """Text styles for the CLI

    Args:
        IntEnum (_type_): enum type
    """

    GRID = 1
    SHIP = 2
    DESTROYED = 3
    SELECTOR = 4
    ERROR = 5


class CLI:
    def __init__(self) -> None:
        """CLI class"""
        self.screen = curses.initscr()
        self.screen.keypad(True)
        curses.curs_set(0)
        curses.start_color()
        curses.cbreak()
        curses.init_pair(Styles.GRID, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(Styles.SHIP, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(Styles.DESTROYED, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(Styles.SELECTOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(Styles.ERROR, curses.COLOR_RED, curses.COLOR_BLACK)

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

    def _draw_ship(
        self,
        ship: Ship,
        board: Board,
        ship_square_locations: list,
        possible_location: bool = True,
    ) -> None:
        """Draws a ship on the board. It clolors the ship ``config.colors.ErrorColor`` if it's not possible to place it there.

        Args:
            ship (Ship): ship object
            board (Board): board object
            ship_square_locations (list): list of (x, y) locations of the ship
            possible_location (bool, optional): indicates if it's possible to place
            the ship in that location. Defaults to True.
        """
        horizontal_offset = (
            config.BOARD_SIZE + config.DEFAULT_SPACE_BETWEEN_BOARDS
            if board.player.side == 1
            else 0
        )

        for i, location in enumerate(ship_square_locations):
            draw_y = board.size - location[1]
            draw_x = 2 * (horizontal_offset + location[0])

            alive = ship[i]
            color = Styles.SHIP if possible_location else Styles.ERROR
            self.screen.addstr(
                draw_y,
                draw_x,
                "O" if alive else "X",
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
    ):
        """Transforms a given location based on the user input (key) and given boundaries.

        Args:
            key (int): user input key code
            location (tuple): (x, y)
            max_x (int): max x index
            min_x (int): min x index
            max_y (int): max y index
            min_y (int): min y index

        Returns:
            _type_: _description_
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

    def show_board(
        self,
        board: Board,
        hilight: None | tuple = None,
        ommit_locations: list | None = None,
        skip_refresh: bool = False,
    ) -> None:
        """Prints board to the console.

        Args:
            board (Board): The board to be printed
            hilight (None | tuple, optional): (x, y) location to be highlited. Defaults to None.
            ommit_locations (list | None, optional): list of (x, y) locations not to be shown. Defaults to None.
            skip_refresh (bool, optional): Decides of the function will skip the screen refresh. Defaults to False.
        """
        horizontal_offset = (
            config.BOARD_SIZE + config.DEFAULT_SPACE_BETWEEN_BOARDS
            if board.player.side == 1
            else 0
        )

        if not skip_refresh:
            self.screen.clear()

        self.screen.addstr(0, horizontal_offset * 2, board.player.name)

        for i in range(board.size):
            for j in range(board.size):
                cell = board.cell(i, j)
                color = Styles.GRID
                if ommit_locations and (i, j) in ommit_locations or not cell:
                    bold = False
                    symbol = "·"
                else:
                    bold = True
                    if cell.alive:
                        color = Styles.SHIP
                        symbol = "O"
                    else:
                        color = Styles.DESTROYED
                        symbol = "X"
                if hilight and (i, j) == hilight:
                    color = Styles.SELECTOR

                self.screen.addstr(
                    board.size - j,
                    (horizontal_offset + i) * 2,
                    symbol,
                    curses.color_pair(color)
                    | (curses.A_BOLD if bold else curses.A_NORMAL),
                )

        if not skip_refresh:
            self.screen.refresh()

    def get_location(
        self, board: Board, additional_board: Board | None = None
    ) -> tuple:
        """Gets a location from the user

        Args:
            board (Board): board to get the location from
            additional_board (Board, optional): board to be shown but not to be interacted with. Defaults to None

        Returns:
            tuple: (x, y) location
        """
        x, y = 0, 0

        while True:
            self.screen.clear()
            if additional_board:
                self.show_board(board, (x, y), skip_refresh=True)
                self.show_board(additional_board, skip_refresh=True)
                self.screen.refresh()
            else:
                self.show_board(board, (x, y))

            key = self.screen.getch()
            if key == ord("\n"):
                break
            else:
                x, y = self._transform_location(
                    key, (x, y), board.size - 1, 0, board.size - 1, 0
                )

        return (x, y)

    def get_move_ship_data(
        self, ship: Ship, board: Board, additional_board: Board | None = None
    ) -> tuple:
        """Gets the new position and orientation of a ship from user.
        It ensures validity of the data.

        Args:
            ship (Ship): ship to move
            board (Board): board to move the ship on
            additional_board (Board, optional): board to be shown but not to be interacted with. Defaults to None

        Returns:
            tuple: (x, y, orientation)
        """
        location = ship.location
        orientation = ship.orientation
        size = ship.size

        x, y = 0, 0

        ommit_locations = []
        if location:
            ommit_locations = board.calculate_square_locations(
                location, orientation, ship.size
            )
            x, y = location

        while True:
            self.screen.clear()
            if additional_board:
                self.show_board(
                    board, skip_refresh=True, ommit_locations=ommit_locations
                )
                self.show_board(additional_board, skip_refresh=True)
            else:
                self.show_board(
                    board, skip_refresh=True, ommit_locations=ommit_locations
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
