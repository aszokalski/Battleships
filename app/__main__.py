from players import Player

from ui import CLI


player = Player()
enemy = Player()
player.set_enemy(enemy)
enemy.set_enemy(player)

# player.board.add_ship(0, (6, 6), "LEFT")
# player.board.add_ship(1, (3, 3), "RIGHT")
# enemy.enemy_board.attack(6, 6)
cli = CLI()


def loop():
    for ship_uuid, ship in player.ships.items():
        x, y, orientation = cli.get_move_ship_data(ship, player.board)
        player.board.move_ship(ship_uuid, (x, y), orientation)

    (x, y) = cli.get_location(player.board)


loop = cli.wrap(loop)
loop()

cli.close()
