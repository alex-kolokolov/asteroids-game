import pygame
import os
import sys
from sprite_groups import all_spr

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

class Explosion(pygame.sprite.Sprite):

    def __init__(self, *group, size: tuple, coords: tuple):
        super().__init__(*group)
        self.size = size
        self.source = pygame.transform.scale(load_image_1("boom.png"), self.size)
        self.mask = pygame.mask.from_surface(self.source)
        self.image = pygame.transform.scale(self.source, self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx = coords[0]
        self.rect.centery = coords[1]
        self.timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.timer > 1500:
            self.kill()


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()
    Explosion(all_spr, size=(140, 140), coords=(250, 250))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_spr.draw(screen)
        all_spr.update()
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()

