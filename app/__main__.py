from players import Player, AIPlayer
from game import Game

from ui import CLI

cli = CLI()


def loop():
    player = Player(side=0, name="Adam", ui=cli)
    enemy = AIPlayer(side=1, name="AI")
    game = Game(player, enemy)
    game.initialize_boards()
    (x, y) = cli.get_location(player.board, enemy.board)


loop = cli.wrap(loop)
loop()

cli.close()
