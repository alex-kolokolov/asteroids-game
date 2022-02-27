import os
import sys
import pygame
import math
from pygame.math import Vector2
from asteroid import Asteroid
import random
from screensaver import start_screen, terminate
from character import Character, Bullet
from sprite_groups import asteroids, all_spr, bullets, resolution, enemies, bullets_bot, score
from enemy import Enemy, BulletBot

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

pygame.init()
pygame.mixer.init()
bg = pygame.transform.scale(load_image_1('fon.jpg'), resolution)
width, height = resolution
channel1 = pygame.mixer.Channel(0) # argument must be int
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
beat1 = pygame.mixer.Sound("data/beat.ogg")
beat2 =  pygame.mixer.Sound("data/beat-2.ogg")
beat3 = pygame.mixer.Sound("data/beat-3.ogg")
fight = pygame.mixer.Sound("data/saucer-lg.ogg")
screen = pygame.display.set_mode(resolution)
icons = [load_image_1('ship_icon.png') for i in range(3)]
channel2.set_endevent( pygame.USEREVENT+2 )
channel3.set_endevent( pygame.USEREVENT+1 )
prepare_sound = [beat1 for i in range(6)] + [beat2 for i in range(6)] + [beat3 for i in range(6)]
fight_sound = [fight for i in range(15)]
channel3.play(prepare_sound[0])
prepare_sound_index = 1
fight_sound_index = 1


clock = pygame.time.Clock()
if __name__ == '__main__':
    start_screen()
    n = 5
    running = True
    asteroid_delay = 0
    ch = Character(all_spr)
    clock = pygame.time.Clock()
    shoot_delay = 0
    for i in range(n):
        Asteroid(asteroids)

    while running:
        screen.fill([255, 255, 255])
        screen.blit(bg, (0, 0))
        shoot_delay += 1


        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.USEREVENT + 1) and len(enemies) == 0:
                # Channel2 sound ended, start the next sound!
                prepare_sound_index += 1
                if (prepare_sound_index < len(prepare_sound)):
                    channel3.play(prepare_sound[prepare_sound_index])
                    print("Sound ended")

                else:
                    prepare_sound_index = 0
                    en = Enemy(enemies, ch=ch)
                    channel2.play(fight_sound[0])
            elif (event.type == pygame.USEREVENT + 2) and len(enemies) > 0:
                # Channel2 sound ended, start the next sound!
                prepare_sound_index += 1
                if (prepare_sound_index < len(prepare_sound)):
                    channel2.play(fight_sound[fight_sound_index])
                    print("Sound ended")

                else:
                    prepare_sound_index = 0
                    channel3.play(prepare_sound[0])

        if len(all_spr) != 0 and pygame.key.get_pressed()[pygame.K_SPACE] and shoot_delay > 45:
            bul = Bullet(bullets, x=ch.rect.center[0], y=ch.rect.center[1], angle=ch.angle)
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
        text = font.render(f"Score: {sum(score)}", True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()

        text_x = width - text.get_width()
        text_y = text.get_height()
        pygame.draw.rect(screen, (255, 255, 255), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
