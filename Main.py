import pygame

windowWidth = 400
windowHeight = 600
game_side_margin = 10
game_top_margin = 40
game_bottom_margin = game_top_margin
game_border_width = 3

wall_top = game_top_margin + game_border_width
wall_left = game_side_margin + game_border_width
wall_right = windowWidth - game_side_margin - game_border_width
wall_bottom = windowHeight - game_bottom_margin - game_border_width

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

pygame.init()

# load game images
playerImg = pygame.image.load("si-player.gif")
enemyImg = pygame.image.load("si-enemy.gif")
bulletImg = pygame.image.load("si-bullet.gif")
backgroundImg = pygame.image.load("si-background.gif")

# load sounds
laser_sound = pygame.mixer.Sound('si-laser.wav')
explosion_sound = pygame.mixer.Sound('si-explode.wav')
#pygame.mixer.music.load('song2.mp3')
#pygame.mixer.music.play(-1)

title_font = pygame.font.SysFont('Arial', 40, True)
score_font = pygame.font.SysFont('Arial', 26, True)

gameDisplay = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Space Invaders')

class GameObject(object):
    def __init__(self, xcor, ycor, image, speed):
        self.xcor = xcor
        self.ycor = ycor
        self.img = image
        self.speed = speed
        self.width = image.get_width()
        self.height = image.get_height()
    def show(self):
        gameDisplay.blit(self.img, (self.xcor, self.ycor))
    def collides_with(self, foreign_object):
        return foreign_object.xcor < self.xcor + self.width \
            and foreign_object.xcor + foreign_object.width > self.xcor \
            and foreign_object.ycor < self.ycor + self.height \
            and foreign_object.ycor + self.height > self.ycor

class Player(GameObject):
    def __init__(self, xcor, ycor, image, speed):
        super().__init__(xcor, ycor, image, speed)
        self.is_alive = True
        self.direction = 0
        self.score = 0
    def show(self):
        new_xcor = self.xcor + self.direction * self.speed
        if new_xcor < wall_left or new_xcor > wall_right - self.width:
            self.xcor = self.xcor
        else:
            self.xcor = new_xcor
        super().show()
    def move_right(self):
        self.direction = 1
    def move_left(self):
        self.direction = -1
    def stop_moving(self):
        self.direction = 0
    def shoot(self):
        laser_sound.play()
        newBullet = Bullet(self.xcor + self.width / 2 - bulletImg.get_width() / 2, self.ycor - bulletImg.get_height(), bulletImg, 10)
        bullets.append(newBullet)
    def change_score(self, amount_to_change_by):
        self.score += amount_to_change_by

class Enemy(GameObject):
    def __init__(self, xcor, ycor, image, speed):
        super().__init__(xcor, ycor, image, speed)
        self.direction = 1
    def move_over(self):
        self.xcor += self.direction * self.speed
    def move_down(self):
        self.ycor += 15
    def change_direction(self):
        self.direction *= -1

class Bullet(GameObject):
    def __init__(self, xcor, ycor, image, speed):
        super().__init__(xcor, ycor, image, speed)
    def move_up(self):
        self.ycor -= self.speed

clock = pygame.time.Clock()

player1 = Player(wall_left + (wall_right - wall_left) / 2 - playerImg.get_width() / 2, 
    wall_bottom - playerImg.get_height() - 1, playerImg, 5)

enemies = []
bullets = []

for row in range(0, 3):
    for column in range(0, 5):
        newEnemy = Enemy((enemyImg.get_width() + 5) * column + wall_left + 1, \
            (enemyImg.get_height() + 5) * row + wall_top + 1, \
            enemyImg, 2)
        enemies.append(newEnemy)

# main game loop
while player1.is_alive:

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player1.is_alive = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.move_left()
            elif event.key == pygame.K_RIGHT:
                player1.move_right()
            elif event.key == pygame.K_SPACE:
                player1.shoot()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1.stop_moving()

    gameDisplay.blit(gameDisplay, (0,0))
    gameDisplay.fill(black)
    title_text = title_font.render('SPACE INVADERS', False, blue)             # Originally (2, 0)
    gameDisplay.blit(title_text, (windowWidth / 2 - title_text.get_width() / 2, 5))
    score_text = score_font.render('SCORE: ' + str(player1.score), False, white)
    gameDisplay.blit(score_text, (wall_left, wall_bottom + game_border_width))
    pygame.draw.rect(gameDisplay, white, (game_side_margin, game_top_margin, windowWidth - game_side_margin * 2, windowHeight - game_top_margin - game_bottom_margin))
    gameDisplay.blit(backgroundImg, (wall_left, wall_top), (0, 0, wall_right - wall_left, wall_bottom - wall_top))

    # check each bullet to see if it hits an enemy
    for bullet in bullets:
        # check if this bullet has gone off the top
        if bullet.ycor < wall_top:
            bullets.remove(bullet)
            continue

        # check if this bullet has hit any of the enemies
        for enemy in enemies:
            # if the bullet has collided with an enemy, remove both from their arrays
            if bullet.collides_with(enemy):
                explosion_sound.play()
                enemies.remove(enemy)
                bullets.remove(bullet)
                player1.change_score(150)
                break

    # check all enemies to see if one has reached a wall
    for enemy in enemies:
        if enemy.xcor <= wall_left or enemy.xcor >= wall_right - enemy.width:
            # since one enemy has reached a wall, change all enemies directions
            for e in enemies:
                e.change_direction()
                e.move_down()
            # since one enemy has reached a wall, stop checking the others
            break
        
        if enemy.collides_with(player1):
            player1.is_alive = False
    
    player1.show()

    # move and show all enemies
    for enemy in enemies:
        enemy.move_over()
        enemy.show()

    # move and show all bullets
    for bullet in bullets:
        bullet.move_up()
        bullet.show()

    pygame.display.update()
    clock.tick(60)

show_final_screen = True
while show_final_screen:
    score_text = score_font.render('SCORE: ' + str(player1.score), False, white)
    gameDisplay.blit(score_text, (windowWidth / 2 - score_text.get_width() / 2, windowHeight / 2))

    pygame.display.update()

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_final_screen = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_final_screen = False


pygame.quit()

