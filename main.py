"""
Главное пространство для запуска
"""
import pygame as pg
from utility.background import Board
from utility.menu import *
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])
pg.init()
pg.display.set_caption('Меню')
screen = pg.display.set_mode((len_side_screen, len_side_screen))

background = Board(len_side_screen, count_cells)

running = True
while running:
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    background.draw(screen)
    pg.display.flip()
    # pg.color.Color('green')

