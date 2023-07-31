"""
Главное пространство для запуска
"""
import os
import pygame as pg

import utility.menu
from utility.field import Board
from utility.menu import start_screen, level_screen, gameover_screen
from utility.level_system import start_level
import utility.menu
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')
len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])

pg.init()
screen = pg.display.set_mode((len_side_screen, len_side_screen))

running = True

pg.display.set_caption('Меню')
start_screen(screen, len_side_screen, count_cells)

cur_len_snake = 0

while running:
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if utility.menu.menu_index in range(0, 2):
                utility.menu.list_groups_buttons[utility.menu.menu_index].update(pg.mouse.get_pos())
                if utility.menu.menu_index == -1:
                    running = False
                    break
                screen.fill('black')
                if utility.menu.menu_index == 0:
                    pg.display.set_caption('Меню')
                    start_screen(screen, len_side_screen, count_cells)
                elif utility.menu.menu_index == 1:
                    pg.display.set_caption('Выбор уровня')
                    level_screen(screen, len_side_screen, count_cells)
                elif utility.menu.menu_index == 2:
                    gameover_screen(screen, len_side_screen, count_cells, cur_len_snake)
                else:
                    # menu_index >= 3
                    start_level(utility.menu.menu_index - 1)

    # background.draw(screen)
    pg.display.flip()

"""
Рандомную генерацию фруктов можно проводить следующим образом:
1. Сохранять индексы свободных ячеек в отдельный массив.
2. Брать одну / две ячейки на фрукт / фрукт + ключ.
3. Вставлять их.
"""

"""
Стены будут запекаться сразу в ActiveBoard
"""
