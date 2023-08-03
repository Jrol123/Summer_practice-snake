"""
Задний фон.

Для активного заднего фона можно сделать наследуемый класс.
"""
import pygame as pg


class Board:
    """
    Класс для представления заднего фона

    Длины измеряются в пикселях.

    :ivar length: Длина стороны заднего фона. Также является длиной стороны экрана
    :type length: int
    :ivar cell_len: Длина стороны ячейки.
    :type cell_len: int
    :ivar cell_begin_coords: Список левых верхних точек ячеек.
    :type cell_begin_coords: list[list[tuple[int, int]]]

    :param length: Длина стороны заднего фона.
    :type length: int
    :param count_cells: Количество ячеек.
    :type count_cells: int

    """

    def __init__(self, length: int, count_cells: int):
        """
        Инициализация класса.

        Единицы измерения — пиксели.
        :param length: Длина стороны заднего фона.
        :type length: int
        :param count_cells: Количество ячеек.
        :type count_cells: int

        """
        self.length = length
        self.cell_len = length // count_cells

        self.cell_begin_coords = []

        x, y = 0, 0

        for i in range(count_cells):
            self.cell_begin_coords.append([])
            for _ in range(count_cells):
                self.cell_begin_coords[i].append((x, y))
                x += self.cell_len
            x = 0
            y += self.cell_len

    def draw(self, screen: pg.Surface,
             colors: tuple[pg.Color | tuple[int, int, int], pg.Color | tuple[int, int, int]]
             = ((79, 255, 77), (60, 191, 57))) -> None:
        """
        Отрисовывание доски на заданном экране.

        :param screen: Экран, на котором будет выведена доска
        :type screen: pg.Surface
        :param colors: Цвета, использующиеся для отрисовки квадратов доски.
        :type colors: tuple[pg.Color | tuple[int, int, int], pg.Color | tuple[int, int, int]]

        """
        for index_side, side in enumerate(self.cell_begin_coords):
            for index_cell, coord in enumerate(side):
                x, y = coord
                color = colors[(index_side + index_cell) % 2]
                pg.draw.rect(screen, color, (x, y, self.cell_len, self.cell_len), 0)
