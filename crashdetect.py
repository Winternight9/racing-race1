def check_crash(player_x, player_y, enemy_x, enemy_y):
    if enemy_x- 75 < player_x < enemy_x + 75 and enemy_y -100 < player_y < enemy_y + 100: 
        return True
    else:
        return False   