"""
Система уровней.

Здесь располагаются все механики, связаные с генерацией уровня.
"""
import configparser

import pygame as pg
from utility.menu import load_image

tile_images = {
    'wall': load_image('wall-block(r).png')
}

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


def start_level(level):
    level_map = load_level(f'{level}')
    for i, row in enumerate(level_map):
        for j, sym in enumerate(row):
            coord_cell = (cell_len * i, cell_len * j)
            empty_space = []
            walls = []
            head_snake
            tail_snake

            match sym:
                case '.':
                    empty_space.append(coord_cell)
                case 'I':
                    walls.append(coord_cell)
                case 'Z':
                    head_snake = coord_cell
                case 'z':
                    tail_snake = coord_cell


"""
В идеале надо вынести всё взаимодействие с графикой (load_image, etc.) в отдельное место
"""
