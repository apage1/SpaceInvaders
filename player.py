from game_object import GameObject
from bullet import Bullet

class Player(GameObject):
    def __init__(self, xcor, ycor, image, speed):
        super().__init__(xcor, ycor, image, speed)
        self.is_alive = True
        self.direction = 0
        self.score = 0
    def show(self,gameDisplay, wall_left, wall_right):
        new_xcor = self.xcor + self.direction * self.speed
        if new_xcor < wall_left or new_xcor > wall_right - self.width:
            self.xcor = self.xcor
        else:
            self.xcor = new_xcor
        super().show(gameDisplay)
    def move_right(self):
        self.direction = 1
    def move_left(self):
        self.direction = -1
    def stop_moving(self):
        self.direction = 0
    def shoot(self, bullets, bulletImg, laser_sound):
        laser_sound.play()
        newBullet = Bullet(self.xcor + self.width / 2 - bulletImg.get_width() / 2, self.ycor - bulletImg.get_height(), bulletImg, 10)
        bullets.append(newBullet)
    def change_score(self, amount_to_change_by):
        self.score += amount_to_change_by