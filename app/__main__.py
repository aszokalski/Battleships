from players import Player, AIPlayer
from game import Game
from ui import CLI
from config import config
from cli_config import icon_ascii_art

cli = CLI()


def loop():
    option = cli.show_menu(
        icon_ascii_art,
        {
            "Player vs Computer": 0,
            "Player vs Player": 1,
            "Settings": 2,
        },
    )

    if option == 0:
        player_name = cli.input("Please enter your name: ")
        player = Player(side=config.DEFAULT_PLAYER_SIDE, name=player_name, ui=cli)
        enemy = AIPlayer(side=1 - config.DEFAULT_PLAYER_SIDE, name="AI")
    elif option == 1:
        player_1_name = cli.input("Please enter the name of Player 1: ")
        player_2_name = cli.input("Please enter the name of Player 2: ")
        player = Player(side=0, name=player_1_name, ui=cli)
        enemy = Player(side=1, name=player_2_name, ui=cli)
    else:
        cli.show_settings()
        loop()
        return

    game = Game(player, enemy)

    game.initialize_boards()
    game_result = game.start()
    winner = player.name if game_result else enemy.name

    cli.show_menu(
        f"Player {winner} won!",
        {"Play again": loop, "Exit": lambda: None},
    )()


loop = cli.wrap(loop)
loop()

cli.close()
