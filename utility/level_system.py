"""
Система уровней.

Здесь располагаются все механики, связаные с генерацией уровня.
"""
import configparser
import pygame as pg

import Game_modules.game_module

config = configparser.ConfigParser()
config.read('config.cfg')
len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])
cell_len = len_side_screen // count_cells


def load_level(filename: str) -> list[list[str]]:
    """
    Функция считывания уровня.

    Файл должен находится в папке levels и иметь название, по типу level_n.txt.

    :param filename: Название считываемого файла.
    :type filename: str
    :return: Двумерный массив карты уровня.
    :rtype: list[list[str]]

    """
    filename = "levels/level_" + filename + ".txt"
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = []
        for j in range(count_cells):
            line = mapFile.readline()
            line = line.replace('\n', '')
            level_map.append([])
            for sym in line:
                level_map[j].append(sym)

        speed, fruit_step, accel = map(int, mapFile.readline().split())

        Game_modules.game_module.speed_movement = speed
        Game_modules.game_module.fruit_step = fruit_step
        Game_modules.game_module.accel = accel

    return level_map


def start_level(screen: pg.Surface, level: int) -> int:
    """
    Функция начала уровня.

    :param screen: Экран, на котором будет происходить отображение уровня.
    :type screen: pg.Surface
    :param level: Номер уровня
    :type level: int
    :return: Номер уровня. #issue 53
    :rtype: int

    """
    empty_space = []
    walls_pos = []
    head_snake = ()
    tail_snake = ()
    exit_pos = ()

    level_map = load_level(f'{level}')

    for i in range(count_cells):
        row = level_map[i]
        for j, sym in enumerate(row):
            coord_cell = (cell_len * j, cell_len * i)

            match sym:
                case '.':
                    empty_space.append(coord_cell)
                case 'I':
                    walls_pos.append(coord_cell)
                case 'Z':
                    head_snake = coord_cell
                    empty_space.append(coord_cell)
                case 'z':
                    tail_snake = coord_cell
                    empty_space.append(coord_cell)
                case 'e':
                    exit_pos = coord_cell

    game = Game_modules.game_module.Game(screen, empty_space, walls_pos, head_snake, tail_snake, exit_pos)
    return game.game_loop()


"""
В идеале надо вынести всё взаимодействие с графикой (load_image, etc.) в отдельное место
"""
