import os
import sys
import pygame
import math
from pygame.math import Vector2
from sprite_groups import asteroids, all_spr, bullets
import random
from explosion import Explosion

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


class Character(pygame.sprite.Sprite):
    def __init__(self, *group):
        self.bg = load_image("fon.jpg")
        self.image_1 = load_image("boom.png")
        super().__init__(*group)
        self.source = pygame.transform.scale(load_image("ship.png"), (140, 140))
        self.mask = pygame.mask.from_surface(self.source)
        self.image = pygame.transform.scale(self.source, (140, 140))
        self.rect = self.image.get_rect()
        self.rect.centerx = 200
        self.rect.centery = 200
        self.time = None
        self.time_1 = None

        self.size = 0
        self.angle = 0
        self.alpha = 255
        offset = Vector2(40, 0).rotate(self.angle)
        self.accel = Vector2(0.1, 0).rotate(self.angle - 90)
        self.dir = Vector2(0, 0)
        self.k = 0.3
        self.pos = Vector2(self.rect.centerx, self.rect.centery) + offset

        self.move = {pygame.K_LEFT: (+1.25, 0),
                     pygame.K_RIGHT: (-1.25, 0),
                     pygame.K_UP: (0, -1),
                     pygame.K_DOWN: (0, +1),
                     pygame.K_SPACE: (+1, 0)}
        # print(self.angle, (self.angle - 90) % 360)

    def rot(self, a):
        self.angle = (self.angle + a) % 360
        self.image = pygame.transform.rotate(self.source, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.accel = Vector2(0.1, 0).rotate(360 - self.angle - 90)
        # print(self.angle, (360 - self.angle - 90)

    def update(self):

        for i in self.move:

            if pygame.key.get_pressed()[i] and (i == pygame.K_DOWN or i == pygame.K_UP):
                # print(self.angle)

                self.dir += self.accel * self.k
                #      print(self.velocity)
                if self.dir.length() > 2.6:
                    self.dir.scale_to_length(1.6)

            elif pygame.key.get_pressed()[i] and (i == pygame.K_LEFT or i == pygame.K_RIGHT):
                self.rot(self.move[i][0])
                self.k = 0.3
            #     print(self.velocity)
        if self.dir[0] != 0 or self.dir[1] != 0:
            self.pos += self.dir  # Add velocity to pos to move the sprite.
            self.rect.center = self.pos  # Update rect coords.
            self.dir -= self.dir * 0.00000005
        else:
            dir = [0, 0]
        if self.time_1 is None:
            if self.size == 0 or self.size == 1:
                if pygame.sprite.spritecollideany(self, asteroids):
                    pygame.sprite.spritecollideany(self, asteroids).kill()

                    self.size += 1
                    self.time_1 = pygame.time.get_ticks()
                    self.time_2 = pygame.time.get_ticks()
            else:
                if pygame.sprite.spritecollideany(self, asteroids):
                    pygame.sprite.spritecollideany(self, asteroids).kill()
                    pygame.transform.scale(self.image_1, (150, 150))
                    self.exp = Explosion(all_spr, size=(140, 140), coords=(self.rect.centerx, self.rect.centery))
                    self.kill()
        else:  # If the timer has been started...
            # and 500 ms have elapsed, kill the sprite.
            self.image.set_alpha(100)
            print(123)
            if pygame.time.get_ticks() - self.time_1 >= 2500:
                self.time_1 = None
                self.image.set_alpha(255)
        print(pygame.time.get_ticks())


class Bullet(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, angle):
        self.image_1 = load_image("boom.png")
        super().__init__(*group)
        self.source = pygame.transform.scale(load_image("bullet.png"), (25, 10))
        self.image = pygame.transform.scale(self.source, (25, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = angle
        offset = Vector2(40, 0).rotate(self.angle)
        self.pos = Vector2(self.rect.centerx, self.rect.centery) + offset
        self.image = pygame.transform.rotate(self.source, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.pos += Vector2(10, 0).rotate(360 - self.angle - 90)
        self.rect.center = self.pos
        if -100 < self.pos[0] > width + 100 or -100 < self.pos[1] > height + 100:
            self.kill()
        return 0
