from players import Player


class Game:
    def __init__(self, playerA: Player, playerB: Player) -> None:
        playerA.set_enemy(playerB)
        playerB.set_enemy(playerA)
        self._playerA = playerA
        self._playerB = playerB

    def initialize_boards(self) -> None:
        """Initialize boards for the players"""
        self._playerA.initialize_board()
        self._playerB.initialize_board()

    def start(self) -> None:
        """Main game loop"""
        while any([self._playerA.fleet_strength, self._playerB.fleet_strength]):
            self._playerA.attack_enemy()
            self._playerB.attack_enemy()
