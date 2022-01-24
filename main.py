import os
import sys
import pygame
import math
from pygame.math import Vector2
# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 1300, 1300
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
        self.image = pygame.transform.scale(self.source, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100
        self.rect.centerx = 100
        self.rect.centery = 100
        self.angle = 0
        offset = Vector2(40, 0).rotate(self.angle)
        self.accel = Vector2(0.00001, 0).rotate(self.angle-90)
        self.op_accel = Vector2(-0.002, 0).rotate(self.angle-90)

        self.pos = Vector2(self.rect.centerx, self.rect.centery) + offset
        print(self.angle, (self.angle - 90) % 360)

    def calculat_new_xy(self, x, y, speed, angle_in_radians):
        new_x = x + (speed * math.cos(angle_in_radians))
        new_y = y + (speed * math.sin(angle_in_radians))
        return new_x, new_y

    def rot(self, a):
        self.angle = (self.angle + a) % 360
        self.image = pygame.transform.rotate(self.source, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.accel = Vector2(0.01, 0).rotate(360 - self.angle - 90)
        print(self.angle, (360 - self.angle - 90))

    def update(self, *args):
        if args[0] == pygame.K_DOWN:
            self.rect.centerx += 10
        if args[0] == pygame.K_UP:
            self.rect.centery -= 10
        if args[0] == pygame.K_RIGHT:
            self.angle -= 10

            print(self.image.get_rect())

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
        pygame.K_DOWN: (0, +v)}

clock = pygame.time.Clock()

if __name__ == '__main__':
    running = True
    all_spr = pygame.sprite.Group()
    cur = Chacter(all_spr)
    clock = pygame.time.Clock()
    dir = Vector2(0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
#            if event.type == pygame.KEYDOWN:
#                 v = event.type
#                 all_spr.update(event.key)
        for i in move:

            if pygame.key.get_pressed()[i] and (i == pygame.K_DOWN or i == pygame.K_UP):
                #print(cur.angle)

                dir += cur.accel
                print(cur.velocity)
                screen.fill(pygame.Color("white"))
                screen.blit(cur.image, cur.rect)
                if dir.length() > 1.3:
                    dir.scale_to_length(1.3)

            elif pygame.key.get_pressed()[i] and (i == pygame.K_LEFT or i == pygame.K_RIGHT):
                cur.rot(move[i][0])
                screen.fill(pygame.Color("white"))
                screen.blit(cur.image, cur.rect)
                print(cur.velocity)
                cur.velocity = Vector2(0, 0).rotate(cur.angle - 90)
                print(cur.velocity)
            if dir[0] != 0 or dir[1] != 0:
                cur.pos += dir  # Add velocity to pos to move the sprite.
                cur.rect.center = cur.pos  # Update rect coords.
                dir -= dir * 0.0005
            else:
                dir = [0, 0]

        screen.fill((255, 255, 255))
        all_spr.draw(screen)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
