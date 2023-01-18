import curses

instructions = {
    "positioning": """Use ↑ ↓ → ← to navigate and ⎵ to rotate ↻.
Click ⏎ to position the ship.
Click ⌫ to reposition the previous ship
    """
}


symbols = {
    "ship": "O",
    "shipHit": "X",
    "cell": ".",
}

# (text_color, background_color)
colors = {
    "grid": (curses.COLOR_GREEN, curses.COLOR_BLACK),
    "ship": (curses.COLOR_WHITE, curses.COLOR_BLACK),
    "destroyed": (curses.COLOR_YELLOW, curses.COLOR_BLACK),
    "selector": (curses.COLOR_BLACK, curses.COLOR_WHITE),
    "error": (curses.COLOR_RED, curses.COLOR_BLACK),
}
