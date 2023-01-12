from ships import Ship


class Player:
    def __init__(self) -> None:
        self.ships = {1: Ship(4)}

    pass


class AIPlayer(Player):
    pass
