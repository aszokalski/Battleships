from players import Player


class Game:
    def __init__(self, playerA: Player, playerB: Player) -> None:
        playerA.set_enemy(playerB)
        playerB.set_enemy(playerA)
        self._playerA = playerA
        self._playerB = playerB

    def initialize_boards(self):
        self._playerA.initialize_board()
        self._playerB.initialize_board()
