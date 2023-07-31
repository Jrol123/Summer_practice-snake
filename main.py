"""
Главное пространство для запуска
"""
import pygame as pg
from utility.field import Board
from utility.menu import start_screen
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])
pg.init()
pg.display.set_caption('Меню')
screen = pg.display.set_mode((len_side_screen, len_side_screen))

# background = Board(len_side_screen, count_cells)

running = True
start_screen(screen, len_side_screen, count_cells)
while running:
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
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
