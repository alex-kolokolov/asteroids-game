import os
import sys
import random
import pygame

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
    image.set_colorkey(
        (255, 255, 255))
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("asteroid.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Bomb.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(60, width - 100)
        self.rect.y = random.randrange(61, height - 100)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)
        while pygame.sprite.spritecollideany(self, all_sprites) != self:
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



all_sprites = pygame.sprite.Group()
for i in range(10):
    Bomb(all_sprites)

if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.KEYDOWN:
            #     v = event.type
            #     all_spr.update(event.key
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
