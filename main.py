"""
Главное пространство для запуска игры.
"""
import os
import pygame as pg

import utility.menu
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

len_snake = 0  # Пользователю будет показан 0
last_level = -1

while running:
    """Цикл меню"""
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT or utility.menu.menu_index == -1:
            running = False
            break
        if event.type == pg.MOUSEBUTTONDOWN:
            utility.menu.list_groups_buttons[utility.menu.menu_index].update(pg.mouse.get_pos())
            if utility.menu.menu_index >= 0:
                screen.fill('black')
                if utility.menu.menu_index == 0:
                    pg.display.set_caption('Меню')
                    start_screen(screen, len_side_screen, count_cells)
                elif utility.menu.menu_index == 1:
                    pg.display.set_caption('Выбор уровня')
                    level_screen(screen, len_side_screen, count_cells)
                elif utility.menu.menu_index == 2:
                    pg.display.set_caption(f'Игра окончена!')
                    gameover_screen(screen, last_level, len_side_screen, count_cells, len_snake)
                else:
                    pg.display.set_caption(f'Уровень {utility.menu.menu_index - 3}')
                    last_level = utility.menu.menu_index - 3
                    # menu_index >= 3
                    len_snake = start_level(screen, utility.menu.menu_index - 3)
                    pg.event.post(pg.event.Event(pg.MOUSEBUTTONDOWN))  # Да, костыль. Но ведь работает!

    pg.display.flip()
