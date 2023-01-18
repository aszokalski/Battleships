BOARD_SIZE = 10
DEFAULT_ORIENTATION = "UP"

BOAT_SIZES = {
    "Carrier": 5,
    "Battleship": 4,
    "Destroyer": 3,
    "Submarine": 3,
    "PatrolBoat": 2,
}

DEFAULT_SHIP_SET = [
    (1, "Carrier"),
    (1, "Battleship"),
    (1, "Destroyer"),
    (2, "Submarine"),
    (2, "PatrolBoat"),
]


DEFAULT_PLAYER_SIDE = 0  # 0 - Left, 1 - Right
DEFAULT_SPACE_BETWEEN_BOARDS = 1  # in terminal character widths
