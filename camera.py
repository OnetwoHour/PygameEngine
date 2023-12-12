width, height = 800, 600

class Camera:
    def __init__(self):
        self.x = self.y = 0
        self.speed = 0.1
        self.target = None

    def apply(self, target):
        self.target = target

    def update(self):
        self.x = self.speed * ((self.target.rect.center[0] - width / 2) - self.x)
        self.y = self.speed * ((self.target.rect.center[1] - height / 2) - self.y)

