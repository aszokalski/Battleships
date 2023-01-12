class Player:
    def __init__(self, ships: list = None) -> None:

        if ships:
            self.ships = {ship.uuid: ship for ship in ships}
        else:
            self.ships = {}


class AIPlayer(Player):
    pass
