class Player:
    def __init__(self, ships: list = None) -> None:
        self.ships = {ship.uuid: ship for ship in ships} if ships else {}


class AIPlayer(Player):
    pass
