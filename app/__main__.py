from players import Player, AIPlayer
from game import Game
from ui import CLI

cli = CLI()


def loop():
    # TODO: add player name input
    player = Player(side=0, name="Adam", ui=cli)
    enemy = AIPlayer(side=1, name="AI")
    game = Game(player, enemy)

    game.initialize_boards()
    game_result = game.start()
    winner = player.name if game_result else enemy.name

    cli.show_menu(
        f"Player {winner} won!",
        {"Play again": loop, "Exit": lambda: None},
    )


loop = cli.wrap(loop)
loop()

cli.close()
