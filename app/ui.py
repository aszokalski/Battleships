from boards import Board
from ships import Ship
from typing import Callable, Literal
import curses
from enum import IntEnum


class Styles(IntEnum):
    GRID = 1
    SHIP = 2
    DESTROYED = 3
    SELECTOR = 4
    ERROR = 5


class CLI:
    def __init__(self) -> None:
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

    def show_board(
        self,
        board: Board,
        hilight: None | tuple = None,
        ommit_locations: list | None = None,
        skip_refresh: bool = False,
    ) -> None:
        """Prints board to the console.

        Args:
            board (Board): board to print
        """
        self.screen.clear()
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
                    board.size - j - 1,
                    i * 2,
                    symbol,
                    curses.color_pair(color)
                    | (curses.A_BOLD if bold else curses.A_NORMAL),
                )
        if not skip_refresh:
            self.screen.refresh()

    def get_location(self, board: Board) -> tuple:
        x, y = 0, 0

        while True:
            self.screen.clear()
            self.show_board(board, (x, y))

            key = self.screen.getch()
            if key == curses.KEY_UP and y < board.size - 1:
                y += 1
            elif key == curses.KEY_DOWN and y > 0:
                y -= 1
            elif key == curses.KEY_LEFT and x > 0:
                x -= 1
            elif key == curses.KEY_RIGHT and x < board.size - 1:
                x += 1
            elif key == ord("\n"):
                break
        return (x, y)

    def get_move_ship_data(self, ship: Ship, board: Board):
        location = ship.location
        orientation = ship.orientation
        size = ship.size

        x, y = 0, 0
        possible_location = True

        ommit_locations = []
        if location:
            ommit_locations = board.calculate_square_locations(
                location, orientation, ship.size
            )
            x, y = location

        def calculate_edge_indexes(
            current_orientation: Literal["UP", "DOWN", "LEFT", "RIGHT"]
        ):
            loc_max_y = (
                board.size - ship.size
                if current_orientation == "UP"
                else board.size - 1
            )
            loc_min_y = ship.size - 1 if current_orientation == "DOWN" else 0
            loc_min_x = ship.size - 1 if current_orientation == "LEFT" else 0
            loc_max_x = (
                board.size - ship.size
                if current_orientation == "RIGHT"
                else board.size - 1
            )
            return (loc_max_x, loc_min_x, loc_max_y, loc_min_y)

        while True:
            self.screen.clear()
            self.show_board(board, skip_refresh=True, ommit_locations=ommit_locations)

            # Check if the ship can be placed there
            square_locations = board.calculate_square_locations(
                (x, y), orientation, size
            )
            if any(
                board.cell(*square) is not None and square not in ommit_locations
                for square in square_locations
            ):
                possible_location = False
            else:
                possible_location = True

            # Draw the ship
            for i in range(size):
                if orientation == "UP":
                    draw_y = board.size - 1 - y - i
                    draw_x = 2 * x
                elif orientation == "DOWN":
                    draw_y = board.size - 1 - y + i
                    draw_x = 2 * x
                elif orientation == "LEFT":
                    draw_y = board.size - 1 - y
                    draw_x = 2 * (x - i)
                elif orientation == "RIGHT":
                    draw_y = board.size - 1 - y
                    draw_x = 2 * (x + i)

                alive = ship[i]
                color = Styles.SHIP if possible_location else Styles.ERROR
                self.screen.addstr(
                    draw_y,
                    draw_x,
                    "O" if alive else "X",
                    curses.color_pair(color) | (curses.A_BOLD if i == 0 else 0),
                )

            # Read user input
            key = self.screen.getch()

            max_x, min_x, max_y, min_y = calculate_edge_indexes(orientation)
            if key == curses.KEY_UP and y < max_y:
                y += 1
            elif key == curses.KEY_DOWN and y > min_y:
                y -= 1
            elif key == curses.KEY_LEFT and x > min_x:
                x -= 1
            elif key == curses.KEY_RIGHT and x < max_x:
                x += 1
            elif key == ord(" "):
                orientation_cycle = ["UP", "RIGHT", "DOWN", "LEFT"]
                next_orientation = orientation_cycle[
                    (orientation_cycle.index(orientation) + 1) % 4
                ]
                max_x, min_x, max_y, min_y = calculate_edge_indexes(next_orientation)
                if x in range(min_x, max_x + 1) and y in range(min_y, max_y + 1):
                    orientation = next_orientation

            elif key == ord("\n"):
                if possible_location:
                    return x, y, orientation

            self.screen.refresh()

    def wrap(self, function: Callable):
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
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
