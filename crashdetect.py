def check_crash(player_x, player_y, enemy_x, enemy_y):
    if enemy_x- 73 < player_x < enemy_x + 73 and enemy_y -93 < player_y < enemy_y + 93: 
        return True
    else:
        return False   