import random

import pygame
import sys
import os
import sqlite3
from sprite_groups import resolution, score

FPS = 50
pygame.init()
width, height = resolution
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

level = None


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(None, 40)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2),
                      self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


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
    btn_1 = Button((255, 255, 255), 500, 500, 250, 250, text='Начать Игру')
    btn_1.draw(screen, outline=True)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_1.is_over(pos):
                    level_selector()
                    return level

        pygame.display.flip()
        clock.tick(FPS)


def level_selector():
    text = ["Выберите уровень"]
    fon = pygame.transform.scale(load_image_fon('fon.jpg'), resolution)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    btn_1 = Button((255, 255, 255), 270, 500, 250, 250, text='1 Уровень')
    btn_1.draw(screen, outline=True)
    btn_2 = Button((255, 255, 255), 540, 500, 250, 250, text='2 Уровень')
    btn_2.draw(screen, outline=True)
    btn_3 = Button((255, 255, 255), 810, 500, 250, 250, text='3 Уровень')
    btn_3.draw(screen, outline=True)
    global level
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color(0, 0, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_1.is_over(pos):
                    level = 1
                    return 1
                if btn_2.is_over(pos):
                    level = 2
                    return 2
                if btn_3.is_over(pos):
                    level = 3
                    return 3
        pygame.display.flip()
        clock.tick(FPS)


def stop_screen(level):
    intro_text = ["Вы проиграли"]
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 200
    btn_restart = Button((255, 255, 255), width // 2 - 375, height // 2, 250, 250, text='Вернуться в меню')
    btn_restart.draw(screen, outline=True)
    btn_records = Button((255, 255, 255), width // 2 + 125, height // 2, 250, 250, text='Талица рекордов')
    btn_records.draw(screen, outline=True)

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(250, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - 160
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    with sqlite3.connect("Score.db") as connection:
        connection.cursor().execute(
            f"""INSERT INTO best_score(level, score) VALUES({level}, {sum(score)})""").fetchall()
        connection.commit()

    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_restart.is_over(pos):
                    return start_screen()  # заканчиваем игру
                if btn_records.is_over(pos):
                    record_table()
                    return start_screen()
            btn_restart.draw(screen, outline=True)
        pygame.display.flip()
        clock.tick(FPS)


def record_table():
    btn_restart = Button((255, 255, 255), width // 2 - 125, height // 2 + 100, 250, 250, text='Вернуться в меню')
    btn_restart.draw(screen, outline=True)
    with sqlite3.connect("Score.db") as connection:
        text = connection.cursor().execute(f"""SELECT level, score FROM best_score ORDER BY score DESC""").fetchall()[
               :5]
        connection.commit()
    intro_text = []
    text_coord = 20
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 70)
    intro_text = ['5 Лучших Игр.', 'Уровень: Кол-во очков:']
    for i in intro_text:
        string_rendered = font.render(i, 1, pygame.Color(250, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - 160
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    for line in enumerate(text, 1):
        line = f'{str(line[0])}.' + '    ' + '                  '.join(list(map(lambda x: str(x), line[1])))
        for i in line:
            string_rendered = font.render(line, 1, pygame.Color(250, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - 245
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_restart.is_over(pos):
                    return # заканчиваем игру
            btn_restart.draw(screen, outline=True)
        pygame.display.flip()
        clock.tick(FPS)
