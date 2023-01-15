import curses


def select_index(matrix):
    # Initialize curses
    stdscr = curses.initscr()
    curses.start_color()
    # curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)

    # Create color pair for selected cell
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Get matrix dimensions
    rows, cols = len(matrix), len(matrix[0])

    # Initialize variables to keep track of selected cell
    x, y = 0, 0

    while True:
        # Clear screen
        stdscr.clear()

        # Draw matrix
        for i in range(rows):
            for j in range(cols):
                # Highlight selected cell
                if i == y and j == x:
                    stdscr.addstr(i, j * 2, str(matrix[i][j]), curses.color_pair(1))
                else:
                    stdscr.addstr(i, j * 2, str(matrix[i][j]))

        # Refresh screen
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < rows - 1:
            y += 1
        elif key == curses.KEY_LEFT and x > 0:
            x -= 1
        elif key == curses.KEY_RIGHT and x < cols - 1:
            x += 1
        elif key == ord("\n"):
            # Exit loop if enter is pressed
            break

    # End curses
    curses.endwin()

    return (y, x)


print(select_index([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))


def place_ship(board, ship):
    stdscr = curses.initscr()
    # Get ship length
    ship_length = len(ship)

    # Initialize ship position and rotation
    x, y = 0, 0
    rotation = 0

    while True:
        # Clear screen
        stdscr.clear()

        for i in range(len(board)):
            for j in range(len(board[i])):
                stdscr.addstr(i, j * 2, board[i][j])
                if j < len(board[i]) - 1:
                    stdscr.addstr(i, j * 2 + 1, "|")
            if i < len(board) - 1:
                stdscr.addstr(i + 1, 0, "-" * (len(board[i]) * 2 - 1))

        # Draw ship
        for i in range(ship_length):
            if rotation == 0:
                stdscr.addstr(y + i, x * 2, ship[i])
            elif rotation == 1:
                stdscr.addstr(y, (x + i) * 2, ship[i])
            elif rotation == 2:
                stdscr.addstr((y - i), x * 2, ship[i])
            elif rotation == 3:
                stdscr.addstr(y, (x - i) * 2, ship[i])

        # Refresh screen
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        if key == curses.KEY_UP and y > 0:
            y -= 1
        elif key == curses.KEY_DOWN and y < len(board) - ship_length:
            y += 1
        elif key == curses.KEY_LEFT and x > 0:
            x -= 1
        elif key == curses.KEY_RIGHT and x < len(board[0]) - 1:
            x += 1
        elif key == ord("w"):
            rotation = (rotation - 1) % 4
        elif key == ord("s"):
            rotation = (rotation + 1) % 4
        elif key == ord("a"):
            rotation = (rotation + 2) % 4
        elif key == ord("d"):
            rotation = (rotation - 2) % 4
        elif key == ord("\n"):
            # Exit loop if enter is pressed
            break

    return (y, x, rotation)


print(place_ship([["." for _ in range(10)] for _ in range(10)], ["X", "X", "X"]))
