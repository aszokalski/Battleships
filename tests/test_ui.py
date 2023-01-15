from ui import CLI
from io import StringIO
import sys
from ships import Ship
from players import Player
from boards import Board


# def test_cli_get_player_name(monkeypatch):
#     monkeypatch.setattr("builtins.input", lambda _: "John")
#     cli = CLI()
#     assert cli.get_player_name() == "John"


# def test_cli_get_location(monkeypatch):
#     monkeypatch.setattr("builtins.input", lambda _: "1 2")
#     cli = CLI()
#     assert cli.get_location() == (1, 2)


# def test_cli_get_location_wrong_input(monkeypatch):
#     def input_generator():
#         yield "1, 2"
#         yield "1 2"

#     input_gen = input_generator()
#     monkeypatch.setattr("builtins.input", lambda _: next(input_gen))
#     cli = CLI()
#     assert cli.get_location() == (1, 2)


# def test_cli_show_board():
#     ship = Ship(4)
#     player = Player(ships=[ship])
#     board = Board(player=player)
#     board.add_ship(shipUUID=ship.uuid, location=(3, 4), orientation="RIGHT")
#     board.attack(3, 4)

#     capturedOutput = StringIO()
#     sys.stdout = capturedOutput

#     cli = CLI()
#     cli.show_board(board)

#     sys.stdout = sys.__stdout__

#     assert (
#         capturedOutput.getvalue()
#         == """[ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] \x1b[1m[O]\x1b[0m [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] \x1b[1m[O]\x1b[0m [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] \x1b[1m[O]\x1b[0m [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] \x1b[1m\x1b[93m[X]\x1b[0m\x1b[0m [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
# """
#     )
