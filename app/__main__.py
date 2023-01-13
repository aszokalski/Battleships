from players import Player

player = Player()
enemy = Player()
player.set_enemy(enemy)
enemy.set_enemy(player)

player.board.add_ship(0, (2, 3), "UP")
print(player.board)

enemy.enemy_board.attack(2, 3)
print(player.board)
