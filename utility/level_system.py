"""
Система уровней.

Здесь располагаются все механики, связаные с генерацией уровня.
"""
import configparser
import pygame as pg

import Game_modules.game_module
import utility
from Game_modules import game_module
from utility.menu import load_image

config = configparser.ConfigParser()
config.read('config.cfg')
len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])
cell_len = len_side_screen // count_cells


def load_level(filename: str) -> list[list[str]]:
    filename = "levels/level_" + filename + ".txt"
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = []
        for j, line in enumerate(mapFile):
            level_map.append([])
            for i in range(15):
                level_map[j].append(line[i])

    return level_map


"""
Как правильно загружать уровни?
Если игрок захочет переключиться между уровнями придётся тогда очищать списки?
Или же делать абстрактный класс игра, в котором будут инициализироваться объекты по спискам
"""


def start_level(screen, level):
    empty_space = []
    walls_pos = []
    head_snake = ()
    tail_snake = ()
    exit_pos = ()

    level_map = load_level(f'{level}')

    for i, row in enumerate(level_map):
        for j, sym in enumerate(row):
            coord_cell = (cell_len * j, cell_len * i)

            match sym:
                case '.':
                    empty_space.append(coord_cell)
                case 'I':
                    walls_pos.append(coord_cell)
                case 'Z':
                    head_snake = coord_cell
                case 'z':
                    tail_snake = coord_cell
                case 'e':
                    exit_pos = coord_cell
    Game_modules.game_module.Game().start(screen, empty_space, walls_pos, head_snake, tail_snake, exit_pos)
    # Далее тут будет распознавание начального положения змеи из координат головы и хвоста.


"""
В идеале надо вынести всё взаимодействие с графикой (load_image, etc.) в отдельное место
"""
"""
Стены + выход ставятся однократно
"""
