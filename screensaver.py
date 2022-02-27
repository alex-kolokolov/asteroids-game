import pygame
import sys
import os
from sprite_groups import resolution

FPS = 50
pygame.init()
width, height = resolution
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()


def load_image_fon(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Приветствуем!", "",
                  "Правила игры",
                  "1) Вам предстоит сражаться за свой корабль отстреливаясь от астероидов!",
                  "2) У вас есть три жизни, когда все жизни закончатся вы проиграеие!",
                  "3) За каждый сбитый астероид вам начисляются очки.!",
                  "Желаем вам удачи!",
                  "Нажмите на любую кнопку"]

    fon = pygame.transform.scale(load_image_fon('fon.jpg'), resolution)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(0, 0, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def stop_screen():
    intro_text = [ "К сожалению вы не смогли выжить"]

    fon = pygame.transform.scale(load_image_fon('fon.jpg'), resolution)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(18, 10, 143))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)