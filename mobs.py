import pygame, random
import numpy as np

width, height = 800, 600

red = (255, 0, 0)
blue = (0, 0, 255)

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        pygame.draw.rect(self.image, red, pygame.Rect(0, 0, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 350 
        self.rect.y = 200
        self.abs_pos = [350, 200]
        self.dy = 0
    
    def update(self, pos=(0,0)):
        if self.abs_pos[1] - 50 < height:
            self.dy += 0.3
            self.rect.y += self.dy
            self.abs_pos[1] += self.dy
        else:
            self.dy += 0.05
            self.dy = min(5, self.dy)
            self.rect.y += self.dy
            self.abs_pos[1] += self.dy
        self.rect.x -= pos[0]
        self.rect.y -= pos[1]

class Bot(Player):
    def __init__(self):
        super().__init__()
        pygame.draw.rect(self.image, blue, pygame.Rect(0, 0, 50, 50))
        self.learning_rate = 0.2  # 조정된 학습률
        self.beta1 = 0.98  # Adam의 beta1 파라미터
        self.beta2 = 0.999  # Adam의 beta2 파라미터
        self.epsilon = 1e-8  # Adam의 epsilon 파라미터
        self.moment1 = 0.7  # 초기 1차 모멘텀 (첫 번째 모멘텀)
        self.moment2 = 0  # 초기 2차 모멘텀 (두 번째 모멘텀)
        self.prev_height = 0

    def update(self, pos=(0,0), learn = False, collision = None):
        
        if self.abs_pos[1] < height:
            self.dy += 0.3
            self.rect.y += self.dy
            self.abs_pos[1] += self.dy
        else:
            self.dy += 0.01
            self.rect.y += self.dy
            self.abs_pos[1] += self.dy


        self.rect.x -= pos[0]
        self.rect.y -= pos[1]

        if not learn:
            return

        # 경사 하강법과 유사한 방법으로 이동 (Adam 알고리즘 사용)
        gradient = collision.slope
        if gradient == 0:
            gradient = 1e-10 * random.randrange(-1, 1, 2)

        # 탐험을 위해 무작위로 움직임 추가
        explore_chance = 0.1
        if random.random() < explore_chance:
            self.rect.x -= random.randint(-5, 5)
        else:
            self.moment1 = self.beta1 * self.moment1 + (1 - self.beta1) * (gradient)
            self.moment2 = self.beta2 * self.moment2 + (1 - self.beta2) * ((gradient) ** 2)

            move_distance = (self.learning_rate * self.moment1 / (np.sqrt(self.moment2) + self.epsilon)) * 100

            # 한 번에 10칸씩 이동
            if move_distance > 0:
                self.rect.x += min(move_distance, 10)
            else:
                self.rect.x -= min(abs(move_distance), 10)
