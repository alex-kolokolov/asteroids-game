import os
import sys
import random
import pygame
from sprite_groups import asteroids, all_spr, bullets, enemies, bullets_bot, score
import character
from explosion import Explosion
from character import Bullet
from pygame.math import Vector2
from sprite_groups import resolution
from math import atan2, degrees

pygame.init()
size = width, height = resolution
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    colorkey = image.get_at((1, 1))
    image.set_colorkey(colorkey)
    return image


class Enemy(pygame.sprite.Sprite):

    def __init__(self, *group, ch=None):
        super().__init__(*group)
        self.ch = ch
        self.size = 0
        self.timer = None
        self.vx = random.choice([-1, 1])
        self.vy = random.choice([-1, 1])
        self.source = pygame.transform.scale(load_image("ship2.png"), (100, 100))
        self.mask = pygame.mask.from_surface(self.source)
        self.image = pygame.transform.scale(self.source, (100, 100))
        self.rect = self.source.get_rect()
        self.rect.centerx = random.randint(0, 1280)
        self.rect.centery = random.randint(0, 720)
        self.size = 0
        self.angle = 0
        self.alpha = 255
        offset = Vector2(40, 0).rotate(self.angle)
        self.accel = Vector2(0.01, 0).rotate(self.angle - 90)
        self.dir = Vector2(0, 0)
        self.pos = Vector2(self.rect.centerx, self.rect.centery) + offset

    def rot(self):
        self.angle = degrees(
            atan2(self.ch.rect.center[1] - self.rect.center[1], self.ch.rect.center[0] - self.rect.center[0]))
        self.image = pygame.transform.rotate(self.source, 270 - self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.accel = Vector2(0.01, 0).rotate(360 - self.angle - 90)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        radians = atan2(self.ch.rect.center[1] - self.rect.center[1], self.ch.rect.center[0] - self.rect.center[0])
        mydegrees = degrees(radians)
        if self.rect[1] > height:
            self.rect[1] = 0
        if self.rect[0] > width:
            self.rect[0] = 0
        if self.rect[0] < 0:
            self.rect[0] = width
        if self.rect[1] < 0:
            self.rect[1] = height
        if self.size == 0:
            if pygame.sprite.spritecollideany(self, bullets):
                pygame.sprite.spritecollideany(self, bullets).kill()
                self.size = 1
        else:
            if pygame.sprite.spritecollideany(self, bullets):
                pygame.sprite.spritecollideany(self, bullets).kill()
                self.exp = Explosion(all_spr, coords=(self.rect.centerx, self.rect.centery))
                score.append(200)
                self.kill()
        if self.timer is None:
            self.timer = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - self.timer >= 1500:
                BulletBot(bullets_bot, x=self.rect.center[0], y=self.rect.center[1], angle=270 - mydegrees)
                self.timer = None
        if self.angle != mydegrees:
            self.rot()


class BulletBot(pygame.sprite.Sprite):
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
        self.pos += Vector2(4, 0).rotate(360 - self.angle - 90)
        self.rect.center = self.pos
        if -100 < self.pos[0] > width + 100 or -100 < self.pos[1] > height + 100:
            self.kill()
        return 0
