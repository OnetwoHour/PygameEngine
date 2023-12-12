import pygame, random

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

width, height = 800, 600

# 바닥 클래스
class Ground(pygame.sprite.Sprite):
    def __init__(self, slope):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.slope = slope
        self.init_pos = (0, 0)
        self.dy = 0

    def getColor(self, y):
        if y > height:
            color = blue
        elif y > 0:
            color = green
        else:
            color = white
        return color

    def update(self, pos = (0, 0)):
        self.rect.x -= pos[0]
        self.rect.y -= pos[1]
        self.dy = self.rect.y

class Rectangle(Ground):
    def __init__(self, pos, slope, init_pos):
        super().__init__(slope)
        self.init_pos = init_pos
        self.color = self.getColor(self.init_pos[1])
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, 50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.move_ip(*pos)

class Triangle(Ground):
    def __init__(self, pos, slope, init_pos):
        super().__init__(slope)
        if self.slope == -1:
            self.points = ((0, 0), (50, 50), (0, 50))
        else:
            self.points = ((0, 50), (50, 0), (50, 50))
        self.init_pos = init_pos
        self.color = self.getColor(self.init_pos[1])
        pygame.draw.polygon(self.image, self.color, self.points)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.move_ip(*pos)

class Underground(Ground):
    def __init__(self, x, y, color, slope=0):
        super().__init__(slope)
        self.image = pygame.Surface((50, height + 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, 50, height + 50))
        self.rect.move_ip(x, y + 50)

value_probability = ((50, 30, 20), (25, 50, 25), (20, 30, 50))

def generate_ground(ground = [], pos = (0, 0)):

    if not ground:
        ground.append(Rectangle((350, 200), 0, (350, 200)))
        ground.append(Rectangle((400, 200), 0, (400, 200)))
    
    while ground[-1].rect.x + 50 - pos[0] <= width:
        slope = random.choices((-1, 0, 1), weights=value_probability[ground[-1].slope + 1], k=1)[0]
        position = [ground[-1].rect.x + 50, ground[-1].rect.y]
        init_pos = [ground[-1].init_pos[0] + 50, ground[-1].init_pos[1]]
        
        if ground[-1].slope == -1 and slope != 1:
            position[1] += 50
            init_pos[1] += 50
        elif ground[-1].slope != -1 and slope == 1:
            position[1] -= 50
            init_pos[1] -= 50

        init_pos = tuple(init_pos)

        if slope == 0:
            ground.append(Rectangle(position, slope, init_pos))
        else:
            ground.append(Triangle(position, slope, init_pos))
        
    
    while ground[0].rect.x - pos[0] >= 0:
        slope = random.choices((-1, 0, 1), weights=value_probability[ground[0].slope + 1], k=1)[0]
        position = [ground[0].rect.x - 50, ground[0].rect.y]
        init_pos = [ground[0].init_pos[0] - 50, ground[0].init_pos[1]]
        
        if ground[0].slope == 1 and slope != -1:
            position[1] += 50
            init_pos[1] += 50
        elif ground[0].slope != 1 and slope == -1:
            position[1] -= 50
            init_pos[1] -= 50

        init_pos = tuple(init_pos)

        if slope == 0:
            ground.insert(0, Rectangle(position, slope, init_pos))
        else:
            ground.insert(0, Triangle(position, slope, init_pos))

    underground = []

    for g in ground:
        ug = Underground(g.rect.x, g.rect.y, color=g.color)
        underground.append(ug)

    return ground, underground
