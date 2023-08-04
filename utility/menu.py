"""
Здесь будут содержаться коды ко всем меню.
"""
import configparser

import pygame
import os
import pygame as pg
from utility.field import Board

menu_index = 0
"""
Глобальная переменная, отвечающая за номер экрана, который нужно отобразить.

-1 означает выход из программы.
"""
color1, color2 = pg.color.Color(130, 255, 127), pg.color.Color(96, 186, 93)
color1.hsva = (119, 55, 100, 100)
color2.hsva = (118, 55, 73, 100)

menu_colors = (color1, color2)
"""Цвета для заднего фона меню."""


def load_image(name: str, resize_ch: float = 1) -> pg.Surface:
    """
    Функция загрузки изображений.

    Изображения должны храниться в папке textures и иметь формат png.

    :param name: Имя изображения.
    :type name: str
    :param resize_ch: Во сколько раз нужно увеличить изображение.
    :type resize_ch: float
    :return: Картинка, с нужным размером.
    :rtype: pg.Surface

    """
    fullname = os.path.join('textures', name + ".png")
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
    """
    Класс кнопки.

    Используется для перехода по меню.

    :ivar image: Картинка кнопки.
    :type image: pygame.Surface
    :ivar rect: Прямоугольник картинки.
    :type rect: pygame.Rect
    :ivar level: Номер экрана, на который нужно перейти.
    :type level: int
    :ivar is_game_level: Является ли level — номером уровня.
    :type is_game_level: bool

    """
    def __init__(self, x: int, y: int, image: pygame.Surface, level: int, *group: pygame.sprite.Group,
                 is_game_level: bool = False):
        super().__init__(*group)

        self.image = image
        image_size = image.get_size()
        x -= image_size[0] // 2
        y -= image_size[1] // 2
        self.rect = self.image.get_rect()
        self.level = level
        self.is_game_level = is_game_level

        self.rect.topleft = (x, y)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Проверка на коллизию позиции мыши с кнопкой.

        Если коллизия есть, вызывается set_level.

        :param mouse_pos: Координаты мыши

        """
        if self.rect.collidepoint(mouse_pos):
            self.set_level()

    def set_level(self):
        """
        Установка нужного экрана.

        Вызывается из update.

        """
        global menu_index
        menu_index = self.level
        if self.is_game_level:
            menu_index += 3
        # menu_index = self.level + int(self.is_game_level) * 3


def background_render(screen: pygame.Surface,
                      len_side_screen: int,
                      count_cells: int,
                      colors:
                      tuple[pygame.color.Color | tuple[int, int, int], pygame.color.Color | tuple[int, int, int]]
                      = ((79, 255, 77), (60, 191, 57))) -> None:
    """
    Рендер заднего фона.

    :param screen: Экран, на котором будут выведен фон.
    :type screen: pygame.Surface
    :param len_side_screen: Длина экрана.
    :type len_side_screen: int
    :param count_cells: Количество ячеек.
    :type count_cells: int
    :param colors: Цвета, которыми будет рисоваться фон.
    :type colors: tuple[pygame.color.Color | tuple[int, int, int], pygame.color.Color | tuple[int, int, int]]

    """
    bgrd = Board(len_side_screen, count_cells)
    bgrd.draw(screen, colors)


def start_screen(screen: pygame.Surface, len_side_screen: int, count_cells: int) -> None:
    """
    Начальный экран.

    :param screen: Экран, на котором будут выведен фон.
    :type screen: pygame.Surface
    :param len_side_screen: Длина экрана.
    :type len_side_screen: int
    :param count_cells: Количество ячеек.
    :type count_cells: int

    """
    background_render(screen, len_side_screen, count_cells, menu_colors)

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

    :param screen: Экран, на котором будут выведен фон.
    :type screen: pygame.Surface
    :param len_side_screen: Длина экрана.
    :type len_side_screen: int
    :param count_cells: Количество ячеек.
    :type count_cells: int

    """
    background_render(screen, len_side_screen, count_cells, menu_colors)
    level_screen_buttons.draw(screen)


def gameover_screen(screen: pygame.Surface, level: int, len_side_screen: int, count_cells: int, len_snake: int) -> None:
    """
    Экран проигрыша.

    :param screen: Экран, на котором будут выведен фон.
    :type screen: pygame.Surface
    :param len_side_screen: Длина экрана.
    :type len_side_screen: int
    :param count_cells: Количество ячеек.
    :type count_cells: int
    :param level: Номер уровня, на котором проиграл пользователь.
    :type level: int
    :param len_snake: Длина змеи, перед проигрышем.
    :type len_snake: int

    """
    background_render(screen, len_side_screen, count_cells, menu_colors)
    gameover_screen_buttons.draw(screen)
    text = ["GAME OVER",
            f"You died on level: {level}",
            f'length of a Snake: {len_snake}']
    font = pygame.font.Font(None, 100)
    text_coord = 35
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 25
        intro_rect.top = text_coord
        intro_rect.x = len_side_screen // 2 - string_rendered.get_size()[0] // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


config = configparser.ConfigParser()
config.read('config.cfg')
len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])

level_buttons_resize = 3


"""Возможно, кнопки стоит перенести в функции"""
start_screen_buttons = pg.sprite.Group()
exit_button = Button(len_side_screen // 2, len_side_screen // 2 + ((len_side_screen // 2) // 3) * 2,
                     load_image("end", 7), -1, start_screen_buttons)
start_button = Button(len_side_screen // 2, len_side_screen // 2, load_image("start", 7), 1,
                      start_screen_buttons)

level_screen_buttons = pg.sprite.Group()
level_1_button = Button(len_side_screen // 2 - (len_side_screen // 2) // 3 * 2, len_side_screen // 2,
                        load_image("1", level_buttons_resize), 1, level_screen_buttons, is_game_level=True)
level_2_button = Button(len_side_screen // 2 - (len_side_screen // 2) // 3 * 1, len_side_screen // 2,
                        load_image("2", level_buttons_resize), 2, level_screen_buttons, is_game_level=True)
level_3_button = Button(len_side_screen // 2 - (len_side_screen // 2) // 3 * 0, len_side_screen // 2,
                        load_image("3", level_buttons_resize), 3, level_screen_buttons, is_game_level=True)
level_4_button = Button(len_side_screen // 2 - (len_side_screen // 2) // 3 * -1, len_side_screen // 2,
                        load_image("4", level_buttons_resize), 4, level_screen_buttons, is_game_level=True)
back_button = Button(len_side_screen // 2, len_side_screen // 2 + ((len_side_screen // 2) // 3) * 2,
                     load_image("back", 7), 0, level_screen_buttons)

gameover_screen_buttons = pg.sprite.Group()

list_groups_buttons = [start_screen_buttons, level_screen_buttons, gameover_screen_buttons]
