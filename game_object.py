class GameObject(object):
    def __init__(self, xcor, ycor, image, speed):
        self.xcor = xcor
        self.ycor = ycor
        self.img = image
        self.speed = speed
        self.width = image.get_width()
        self.height = image.get_height()
    def show(self, gameDisplay):
        gameDisplay.blit(self.img, (self.xcor, self.ycor))
    def collides_with(self, foreign_object):
        return foreign_object.xcor < self.xcor + self.width \
            and foreign_object.xcor + foreign_object.width > self.xcor \
            and foreign_object.ycor < self.ycor + self.height \
            and foreign_object.ycor + self.height > self.ycor