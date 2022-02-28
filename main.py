import os
import sys
import pygame
from asteroid import Asteroid
from screensaver import start_screen, stop_screen
from character import Character, Bullet
from sprite_groups import asteroids, all_spr, bullets, resolution, enemies, bullets_bot, score, lives
from enemy import Enemy, BulletBot
from random import choice


# Изображение не получится загрузить
# без предварительной инициализации pygame


def load_image_1(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    colorkey = image.get_at((0, 0))
    image.set_colorkey(
        colorkey)
    return image


level1 = [(5, 0), (6, 0), (7, 0)]
level2 = [(3, 1), (4, 1), (8, 0)]
level3 = [(3, 2), (4, 2), (0, 3)]
pygame.init()
pygame.mixer.init()
bg = pygame.transform.scale(load_image_1('fon.jpg'), resolution)
width, height = resolution
channel1 = pygame.mixer.Channel(0)  # argument must be int
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
sound1 = pygame.mixer.Sound('music/mus-level1.mp3')
sound2 = pygame.mixer.Sound('music/mus-level2.mp3')
sound3 = pygame.mixer.Sound('music/mus-level3.mp3')
music = {1: sound1,
         2: sound2,
         3: sound3}
fire = pygame.mixer.Sound("data/music/fire-a.mp3")
screen = pygame.display.set_mode(resolution)
icons = [load_image_1('ship_icon.png') for i in range(3)]

if __name__ == '__main__':
    level = start_screen()
    running = True
    asteroid_delay = 0
    ch = Character(all_spr)
    clock = pygame.time.Clock()
    shoot_delay = 0
    channel2.play(music[level], -1)

    while running:
        if len(asteroids) + len(enemies) == 0:
            if level == 1:
                for i in range(choice(level1)[0]):
                    Asteroid(asteroids)
            elif level == 2:
                a = choice(level2)
                for i in range(a[0]):
                    Asteroid(asteroids)
                for i in range(a[1]):
                    Enemy(enemies, ch=ch)
            elif level == 3:
                a = choice(level3)
                for i in range(a[0]):
                    Asteroid(asteroids)
                for i in range(a[1]):
                    Enemy(enemies, ch=ch)
        screen.fill([255, 255, 255])
        screen.blit(bg, (0, 0))
        shoot_delay += 1

        if len(all_spr) == 0:
            channel2.stop()

            level = stop_screen(level)
            score = [0]
            for i in asteroids:
                i.kill()
            for i in all_spr:
                i.kill()
            for i in enemies:
                i.kill()
            running = True
            asteroid_delay = 0
            ch = Character(all_spr)
            clock = pygame.time.Clock()
            shoot_delay = 0
            channel2.play(music[level], -1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if len(all_spr) != 0 and pygame.key.get_pressed()[pygame.K_SPACE] and shoot_delay > 30:
            bul = Bullet(bullets, x=ch.rect.center[0], y=ch.rect.center[1], angle=ch.angle)
            channel1.play(fire)

            shoot_delay = 0

        screen.fill([255, 255, 255])
        screen.blit(bg, (0, 0))
        all_spr.update()
        all_spr.draw(screen)
        n = len(asteroids)

        bullets.update()
        bullets.draw(screen)
        bullets_bot.update()
        bullets_bot.draw(screen)
        asteroids.update()
        asteroids.draw(screen)
        enemies.update()
        enemies.draw(screen)

        font = pygame.font.Font(None, 50)
        level_d = font.render(f"Уровень: {level}", True, (255, 255, 255))
        text = font.render(f"Очки: {sum(score)}", True, (255, 255, 255))
        lives_d = font.render(f"Жизней {lives[-1]}", True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        level_w = level_d.get_width()
        level_h = level_d.get_height()
        text_x = width - text.get_width()
        text_y = text.get_height()
        lives_x = 0
        lives_y = 0
        level_x = width // 2 - level_d.get_width() // 2
        level_y = height - 60

        pygame.draw.rect(screen, (255, 255, 255), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)

        screen.blit(text, (text_x, text_y))
        screen.blit(level_d, (level_x, level_y))
        screen.blit(lives_d, (lives_x, lives_y))
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
