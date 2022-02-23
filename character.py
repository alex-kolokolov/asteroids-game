import os
import sys
import pygame
import math
from pygame.math import Vector2
from asteroid import Bomb, all_sprites
import random

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
    return image


class Chacter(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.source = pygame.transform.scale(load_image("ship.png"), (200, 200))
        self.mask = pygame.mask.from_surface(self.source)
        self.image = pygame.transform.scale(self.source, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = 200
        self.rect.centery = 200
        self.rect.centerx = 200
        self.rect.centery = 200
        self.angle = 0
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
                screen.fill(pygame.Color("white"))
                screen.blit(self.image, self.rect)
                if self.dir.length() > 2.6:
                    self.dir.scale_to_length(1.6)

            elif pygame.key.get_pressed()[i] and (i == pygame.K_LEFT or i == pygame.K_RIGHT):
                self.rot(self.move[i][0])
                self.k = 0.3
                screen.fill(pygame.Color("white"))
                screen.blit(self.image, self.rect)
            #     print(self.velocity)
        if self.dir[0] != 0 or self.dir[1] != 0:
            self.pos += self.dir  # Add velocity to pos to move the sprite.
            self.rect.center = self.pos  # Update rect coords.
            self.dir -= self.dir * 0.00000005
        else:
            dir = [0, 0]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, angle):
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
