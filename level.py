from enemy import Enemy

class Level:
    def __init__(self, row_count, col_count, speed, level_number, enemyImg, wall_left, wall_top):
        self.level_number = level_number
        self.enemies = []

        for row in range(0, row_count):
            for col in range(0, col_count):
                #if row % 2 == 0 and col % 2 != 0 or row % 2 != 0 and col % 2 == 0:
                newEnemy = Enemy((enemyImg.get_width() + 5) * col + wall_left + 1, \
                    (enemyImg.get_height() + 5) * row + wall_top + 1, \
                    enemyImg, speed)
                self.enemies.append(newEnemy)

    
