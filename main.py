import os
import sys
import pygame
import math
from pygame.math import Vector2

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
        self.accel = Vector2(0.001, 0).rotate(self.angle - 90)
        self.op_accel = Vector2(-0.002, 0).rotate(self.angle - 90)
        self.pos = Vector2(self.rect.centerx, self.rect.centery) + offset
        print(self.pos)
        self.image = pygame.transform.rotate(self.source, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Chacter(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.source = pygame.transform.scale(load_image("ship.png"), (200, 200))
        self.image = pygame.transform.scale(self.source, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100
        self.rect.centerx = 100
        self.rect.centery = 100
        self.angle = 0
        offset = Vector2(40, 0).rotate(self.angle)
        self.accel = Vector2(10, 0).rotate(self.angle - 90)

        self.pos = Vector2(self.rect.centerx, self.rect.centery) + offset
        # print(self.angle, (self.angle - 90) % 360)

    def rot(self, a):
        self.angle = (self.angle + a) % 360
        self.image = pygame.transform.rotate(self.source, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.accel = Vector2(0.03, 0).rotate(360 - self.angle - 90)
        # print(self.angle, (360 - self.angle - 90)

    def update(self, *args):
        if args[0] == pygame.K_DOWN:
            self.rect.centerx += 10
        if args[0] == pygame.K_UP:
            self.rect.centery -= 10
        if args[0] == pygame.K_RIGHT:
            self.angle -= 10

            #   print(self.image.get_rect())

            self.image = pygame.transform.rotate(self.source, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

            # self.rect.center = self.rect.centerx, self.rect.centery
            # self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.x, self.rect.y)).center)
        if args[0] == pygame.K_LEFT:
            self.image = pygame.transform.rotate(self.image, math.pi / 36)
            self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.x, self.rect.y)).center)


v = 1
move = {pygame.K_LEFT: (+1.25, 0),
        pygame.K_RIGHT: (-1.25, 0),
        pygame.K_UP: (0, -v),
        pygame.K_DOWN: (0, +v),
        pygame.K_SPACE: (+v, 0)}

clock = pygame.time.Clock()

if __name__ == '__main__':
    running = True
    all_spr = pygame.sprite.Group()

    cur = Chacter(all_spr)
    clock = pygame.time.Clock()
    dir = Vector2(0, 0)
    vel = Vector2(2.5, 0)
    bullets = pygame.sprite.Group()
    shoot_delay = 0
    k = 0.3
    while running:
        shoot_delay += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #            if event.type == pygame.KEYDOWN:
        #                 v = event.type
        #                 all_spr.update(event.key)
        for i in move:

            if pygame.key.get_pressed()[i] and (i == pygame.K_DOWN or i == pygame.K_UP):
                # print(cur.angle)

                dir += cur.accel * k
                if k < 1:
                    k += 0.01
                print(dir)
                #      print(cur.velocity)
                screen.fill(pygame.Color("white"))
                screen.blit(cur.image, cur.rect)
                if dir.length() > 2.6:
                    dir.scale_to_length(1.6)

            elif pygame.key.get_pressed()[i] and (i == pygame.K_LEFT or i == pygame.K_RIGHT):
                cur.rot(move[i][0])
                k = 0.3
                screen.fill(pygame.Color("white"))
                screen.blit(cur.image, cur.rect)
            elif pygame.key.get_pressed()[i] and (i == pygame.K_SPACE) and shoot_delay > 45:

                print(cur.rect.center)
                bul = Bullet(bullets, x=cur.rect.center[0], y=cur.rect.center[1], angle=cur.angle)
                print([i for i in all_spr])
                print(cur.pos)
                print(cur.rect.center)
                shoot_delay = 0
            #     print(cur.velocity)
        if dir[0] != 0 or dir[1] != 0:
            cur.pos += dir  # Add velocity to pos to move the sprite.
            cur.rect.center = cur.pos  # Update rect coords.
            dir -= dir * 0.00000005
        else:
            dir = [0, 0]

        for j in bullets:
            j.pos += Vector2(3, 0).rotate(360 - j.angle - 90)
            j.rect.center = j.pos
            if -100 < j.pos[0] > width + 100 or -100 < j.pos[1] > height + 100:
                j.kill()
                bullets.remove(j)


        screen.fill((255, 255, 255))
        all_spr.draw(screen)
        bullets.draw(screen)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
