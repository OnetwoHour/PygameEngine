import pygame
import pygame
from camera import *
from mobs import *
from ground import *

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Not Real Engine")


# 게임 루프
def game_loop():
    player = Player()
    camera = Camera()
    camera.apply(player)
    clock = pygame.time.Clock()
    ground, underground = generate_ground()
    ground_sprites = pygame.sprite.Group(*ground)
    underground_sprites = pygame.sprite.Group(*underground)
    player_sprites = pygame.sprite.Group(player)
    visible_area = pygame.Rect(0, 0, width, height)
    sea = pygame.Rect(0, height + 50, width, 10000)

    bot = Bot()
    bot_sprites = pygame.sprite.Group(bot)
    collision = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        camera.update()
        ground, underground = generate_ground(ground, underground, (camera.x, camera.y))
        ground_sprites = pygame.sprite.Group(*ground)
        underground_sprites = pygame.sprite.Group(*underground)
        ground_sprites.update((camera.x, camera.y))
        underground_sprites.update((camera.x, camera.y))
        player_sprites.update((camera.x, camera.y))
        sea.y -= camera.y

        screen.fill(black)
        ground_in_area = [sprite for sprite in ground_sprites if visible_area.colliderect(sprite.rect)]
        underground_in_area = [sprite for sprite in underground_sprites if visible_area.colliderect(sprite.rect)]

        ground_collision = pygame.sprite.spritecollide(player, ground_in_area, False, pygame.sprite.collide_mask)

        if ground_collision:
            player.dy = -player.dy * 0.6

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.rect.x += 5
            player.abs_pos[0] += 5
        elif keys[pygame.K_LEFT]:
            player.rect.x -= 5
            player.abs_pos[0] -= 5
        elif keys[pygame.K_UP]:
            if sea.colliderect(player.rect):
                player.dy -= 0.7
                player.dy = max(player.dy, -1.5)
            elif ground_collision:
                player.dy -= 10
                player.dy = max(player.dy, -15)
        elif keys[pygame.K_1]:
            camera.apply(bot)
        elif keys[pygame.K_2]:
            camera.apply(player)


        while ground_collision:
            player.rect.y -= 1
            player.abs_pos[1] -= 1
            ground_collision = pygame.sprite.spritecollide(player, ground_in_area, False, pygame.sprite.collide_mask)
        
        if pygame.sprite.spritecollide(bot, ground_in_area, False, pygame.sprite.collide_mask):
            update = True
            collision = pygame.sprite.spritecollide(bot, ground_in_area, False, pygame.sprite.collide_mask)[0]
        else:
            update = False

        while pygame.sprite.spritecollide(bot, ground_in_area, False, pygame.sprite.collide_mask):
            bot.rect.y -= 1
            bot.abs_pos[1] -= 1
            bot.dy = 0
        
        bot_sprites.update((camera.x, camera.y), update, collision)

        pygame.draw.rect(screen, (0, 0, 120), sea)
        underground_sprites.draw(screen, underground_in_area)
        ground_sprites.draw(screen, ground_in_area)
        player_sprites.draw(screen)
        bot_sprites.draw(screen)
        

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    game_loop()