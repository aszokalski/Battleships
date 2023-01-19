import curses

instructions = {
    "positioning": {
        "title": "Position your ship on the map",
        "instructions": """Use ↑ ↓ → ← to navigate and ⎵ to rotate ↻.
Click ⏎ to position the ship.
Click ⌫ to reposition the previous ship
    """,
    },
    "positioning_random": {
        "title": "Position your ship on the map",
        "instructions": """Use ↑ ↓ → ← to navigate and ⎵ to rotate ↻.
Click ⏎ to position the ship.
Click ⌫ to reposition the previous ship
Click 'r' to randomize the board
    """,
    },
    "editing": {
        "title": "Select the ship you want to move.",
        "instructions": """Use ↑ ↓ → ← to navigate.
Click ⏎ to select the ship.
Click ⌫ to abort.
""",
    },
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
