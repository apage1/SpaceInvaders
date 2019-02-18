import pygame

windowWidth = 400
windowHeight = 600


pygame.init()

gameDisplay = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Space Invaders')

class Player:
    def __init__(self, xcor, ycor, image, speed):
        self.is_alive = True
        self.xcor = xcor
        self.ycor = ycor
        self.img = image
        self.speed = speed
        self.width = image.get_width()
        self.height = image.get_height()
    def show(self):
        gameDisplay.blit(self.img, (self.xcor, self.ycor))

clock = pygame.time.Clock()

playerImg = pygame.image.load("si-player.gif")

player1 = Player(200, 200, playerImg, 5)

while player1.is_alive:

    for event in pygame.event.get():
        #print(str(event))
        if event.type == pygame.QUIT:
            player1.is_alive = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.xcor -= player1.speed
            elif event.key == pygame.K_RIGHT:
                player1.xcor += player1.speed

    player1.show()

    pygame.display.update()

    clock.tick(60)

pygame.quit()