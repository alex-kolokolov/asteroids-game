import pygame
import os
import sys
from sprite_groups import all_spr
import  random

pygame.init()
pygame.mixer.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


def load_image_1(name, colorkey=None):
    fullname = os.path.join('anim', name)
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

    def __init__(self, *group, coords: tuple):
        super().__init__(*group)
        self.sizes = {'boom0': (70, 70),
                      'boom1': (85, 85),
                      'boom2': (100, 100),
                      'boom3': (100, 100),
                      'boom4': (100, 100),
                      'boom5': (100, 100),
                      'boom6': (96, 96),
                      'boom7': (85, 85),
                      'boom8': (70, 70),
                      'boom9': (63, 63),
                      'boom10': (40, 40),
                      'boom11': (20, 20)}
        self.timer = 0
        self.shot = 0
        self.source = pygame.transform.scale(load_image_1("boom0.png"), self.sizes['boom0'])
        self.mask = pygame.mask.from_surface(self.source)
        self.image = pygame.transform.scale(self.source, self.sizes['boom0'])
        self.rect = self.image.get_rect()
        self.rect.centerx = coords[0]
        self.rect.centery = coords[1]
        self.timer = pygame.time.get_ticks()
        sound1 = pygame.mixer.Sound('music/exp-lg.mp3')
        sound2 = pygame.mixer.Sound('music/exp-med.mp3')
        sound3 = pygame.mixer.Sound('music/exp-small.mp3')
        random.choice([sound1, sound2, sound3]).play()

    def update(self):
        print(self.shot)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        else:
            if self.shot < 12:
                if pygame.time.get_ticks() - self.timer > 65:
                    self.source = pygame.transform.scale(load_image_1(f"boom{self.shot}.png"), self.sizes[f'boom{self.shot}'])
                    self.image = pygame.transform.scale(self.source, self.sizes[f'boom{self.shot}'])
                    self.shot += 1
                    self.timer = 0
            else:
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
