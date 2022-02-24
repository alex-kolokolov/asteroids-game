import os
import sys
import random
import pygame
from sprite_groups import asteroids, all_spr, bullets
import character
import screensaver
from explosion import Explosion

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


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


class Asteroid(pygame.sprite.Sprite):
    image = load_image_1("asteroid.png")
    image_1 = load_image_1("boom.png")


    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.size = 0
        self.image = Asteroid.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(60, width - 100)
        self.rect.y = random.randrange(61, height - 100)
        self.vx = random.randint(-3, 3)
        self.vy = random.randrange(-3, 3)
        while pygame.sprite.spritecollideany(self, asteroids) != self:
            self.rect.x = random.randrange(60, width - 100)
            self.rect.y = random.randrange(61, height - 100)


    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect[1] > 600:
            self.rect[1] = 0
        if self.rect[0] > 800:
            self.rect[0] = 0
        if self.rect[0] < 0:
            self.rect[0] = 800
        if self.rect[1] < 0:
            self.rect[1] = 600
        if self.size == 0:
            if pygame.sprite.spritecollideany(self, bullets):
                pygame.sprite.spritecollideany(self, bullets).kill()
                self.size = 1
        else:
            if pygame.sprite.spritecollideany(self, bullets):
                pygame.sprite.spritecollideany(self, bullets).kill()
                self.exp = Explosion(all_spr, size=(140, 140), coords=(self.rect.centerx, self.rect.centery))
                self.kill()

if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()
    character.Character(all_spr)
    for i in range(10):
        Asteroid(asteroids)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.KEYDOWN:
            #     v = event.type
            #     all_spr.update(event.key
        screen.fill((255, 255, 255))
        all_spr.draw(screen)
        all_spr.update()
        asteroids.draw(screen)
        asteroids.update()
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
