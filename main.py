"""
Главное пространство для запуска
"""
import os
import pygame as pg

import utility.menu
from utility.field import Board
from utility.menu import start_screen, level_screen, gameover_screen, Button
import configparser


def exit(*args):
    global menu_index
    menu_index = -1

def start(*args):
    global menu_index
    menu_index = 1


def load_image(name, resize_ch=1):
    fullname = os.path.join('textures', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if resize_ch != 1:
        img_size = image.get_size()
        new_img = (img_size[0] * resize_ch, img_size[1] * resize_ch)
        image = pg.transform.scale(image, new_img)
    return image


config = configparser.ConfigParser()
config.read('config.cfg')

len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])
pg.init()
pg.display.set_caption('Меню')
screen = pg.display.set_mode((len_side_screen, len_side_screen))

running = True
menu_index = 0

exit_img = pg.image.load('textures/end.png')
img_size = exit_img.get_size()
new_exit = (img_size[0] * 5, img_size[1] * 5)

start_screen_buttons = pg.sprite.Group()
level_screen_buttons = pg.sprite.Group()
gameover_screen_buttons = pg.sprite.Group()
exit_button = Button(len_side_screen // 2, len_side_screen // 2 + ((len_side_screen // 2) // 3) * 2,
                     load_image("end.png", 7), exit,  start_screen_buttons)
start_button = Button(len_side_screen // 2, len_side_screen // 2, load_image("start.png", 7), start,  start_screen_buttons)

start_screen(screen, len_side_screen, count_cells)
start_screen_buttons.draw(screen)

list_groups_buttons = [start_screen_buttons, level_screen_buttons, gameover_screen_buttons]

cur_len_snake = 0

while running:
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            list_groups_buttons[menu_index].update(pg.mouse.get_pos())
            if menu_index == -1:
                running = False
                break
            screen.fill('black')
            if menu_index == 0:
                start_screen(screen, len_side_screen, count_cells)
            elif menu_index == 1:
                level_screen(screen, len_side_screen, count_cells)
            elif menu_index == 2:
                gameover_screen(screen, len_side_screen, count_cells, cur_len_snake)


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
