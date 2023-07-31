"""
Здесь будут содержаться коды ко всем меню (см. Milestone Механики)
"""
import configparser

import pygame
import os
import pygame as pg
from utility.field import Board

menu_index = 0


def exit():
    global menu_index
    menu_index = -1
    print(-1)


def main_menu():
    global menu_index
    menu_index = 0


def start():
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


class Button(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface, action, *group: pygame.sprite.Group):
        super().__init__(*group)

        self.action = action

        self.image = image
        image_size = image.get_size()
        x -= image_size[0] // 2
        y -= image_size[1] // 2
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

    def update(self, mouse_pos) -> int | None:
        if self.rect.collidepoint(mouse_pos):
            return self.action()


def background_render(screen: pygame.Surface, len_side_screen: int, count_cells: int) -> None:
    bgrd = Board(len_side_screen, count_cells)
    bgrd.draw(screen)


def start_screen(screen: pygame.Surface, len_side_screen: int, count_cells: int) -> None:
    """
    Начальный экран.

    """
    background_render(screen, len_side_screen, count_cells)

    start_screen_buttons.draw(screen)

    intro_text = ["Snake 2.0"]
    font = pygame.font.Font(None, 100)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = len_side_screen // 2 - string_rendered.get_size()[0] // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def level_screen(screen: pygame.Surface, len_side_screen: int, count_cells: int) -> None:
    """
    Экран выбора уровней

    :param screen:
    :param len_side_screen:
    :param count_cells:

    """
    background_render(screen, len_side_screen, count_cells)
    level_screen_buttons.draw(screen)


def gameover_screen(screen: pygame.Surface, len_side_screen: int, count_cells: int, len_snake: int) -> None:
    pass


config = configparser.ConfigParser()
config.read('config.cfg')
len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])

start_screen_buttons = pg.sprite.Group()
level_screen_buttons = pg.sprite.Group()
gameover_screen_buttons = pg.sprite.Group()
exit_button = Button(len_side_screen // 2, len_side_screen // 2 + ((len_side_screen // 2) // 3) * 2,
                     load_image("end.png", 7), exit, start_screen_buttons)
start_button = Button(len_side_screen // 2, len_side_screen // 2, load_image("start.png", 7), start,
                      start_screen_buttons)

list_groups_buttons = [start_screen_buttons, level_screen_buttons, gameover_screen_buttons]
