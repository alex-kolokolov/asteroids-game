import os
import sys
import random
import pygame
from sprite_groups import asteroids, all_spr, bullets, resolution, score
import character
import screensaver
from explosion import Explosion

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
resolution = width, height = resolution
screen = pygame.display.set_mode(resolution)

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

    def __init__(self, *group, phase=0, x=random.randrange(60, width - 100),
                 y=random.randrange(61, height - 100)):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.size = [(80, 80), (60, 60), (40, 40)]
        self.phase = phase
        self.size = self.size[self.phase]
        self.image = pygame.transform.scale(load_image_1("asteroid.png"), self.size)
        self.image_1 = load_image_1("boom.png")
        self.image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = random.choice([-1, 1])
        self.vy = random.choice([-1, 1])
        if self.phase == 0:
            while pygame.sprite.spritecollideany(self, asteroids) != self and \
                    pygame.sprite.spritecollideany(self, all_spr) != self:
                self.rect.x, self.rect.y = random.choice([(random.choice([60, width - 100]),
                                                           random.randrange(61, height - 100)),
                                                          (random.randrange(61, height - 100),
                                                           random.choice([60, width - 100]))])

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect[1] > height:
            self.rect[1] = 0
            self.rect[0] -= random.randrange(-20, 20)
        if self.rect[0] > width:
            self.rect[0] = 0
            self.rect[1] -= random.randrange(-20, 20)
        if self.rect[0] < 0:
            self.rect[0] = width
            self.rect[1] -= random.randrange(-20, 20)
        if self.rect[1] < 0:
            self.rect[1] = height
            self.rect[0] -= random.randrange(-20, 20)
        if self.phase < 2:
            if pygame.sprite.spritecollideany(self, bullets):
                pygame.sprite.spritecollideany(self, bullets).kill()
                score.append(50)
                Asteroid(asteroids, phase=self.phase + 1, x=self.rect.x, y=self.rect.y)
                Asteroid(asteroids, phase=self.phase + 1, x=self.rect.centerx, y=self.rect.centery)
                self.kill()

        else:
            if pygame.sprite.spritecollideany(self, bullets):
                score.append(50)
                pygame.sprite.spritecollideany(self, bullets).kill()
                Explosion(all_spr, size=(140, 140), coords=(self.rect.centerx, self.rect.centery))
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
