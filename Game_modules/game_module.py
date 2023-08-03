"""
Игровой модуль.

Содержит всю игровую логику.
"""
import configparser
import pygame as pg
import utility.level_system
import utility.menu
import random

config = configparser.ConfigParser()
config.read('config.cfg')
len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])
speed_movement = 500
"""Скорость такта передвижения змеи"""
fruit_step = 6
"""Сколько должно пройти фруктов перед особым фруктом -1"""
accel = 6
"""Раз в какое кол-во фруктов скорость такта уменьшается на 1"""
len_cell = len_side_screen // count_cells

tile_images = {
    'wall': utility.menu.load_image('wall-block(r)', 2),
    'apple': utility.menu.load_image('apple', 1.6),
    'apple_cage': utility.menu.load_image('apple_cage', 1.6),
    'key': utility.menu.load_image('key', 2)
}
"""Изображения предметов"""
head_images = {
    (1, 0): utility.menu.load_image('head_right', 1.6),
    (-1, 0): utility.menu.load_image('head_left', 1.6),
    (0, -1): utility.menu.load_image('head_up', 1.6),
    (0, 1): utility.menu.load_image('head_down', 1.6)
}
"""Изображения головы"""
# issue #50
tail_images = {
    (-1, 0): utility.menu.load_image('tail_right', 1.6),
    (1, 0): utility.menu.load_image('tail_left', 1.6),
    (0, 1): utility.menu.load_image('tail_up', 1.6),
    (0, -1): utility.menu.load_image('tail_down', 1.6)
}
"""Изображения хвоста"""
# Для отображения хвоста берётся только направление его "предыдущего" блока
body_images = {
    ((1, 0), (1, 0)): utility.menu.load_image('body_horizontal', 1.6),
    ((-1, 0), (-1, 0)): utility.menu.load_image('body_horizontal', 1.6),
    ((0, 1), (0, 1)): utility.menu.load_image('body_vertical', 1.6),
    ((0, -1), (0, -1)): utility.menu.load_image('body_vertical', 1.6),
    ((0, -1), (1, 0)): utility.menu.load_image('body_br', 1.6),
    ((-1, 0), (0, 1)): utility.menu.load_image('body_br', 1.6),
    ((1, 0), (0, 1)): utility.menu.load_image('body_bl', 1.6),
    ((0, -1), (-1, 0)): utility.menu.load_image('body_bl', 1.6),
    ((0, 1), (1, 0)): utility.menu.load_image('body_tr', 1.6),
    ((-1, 0), (0, -1)): utility.menu.load_image('body_tr', 1.6),
    ((1, 0), (0, -1)): utility.menu.load_image('body_tl', 1.6),
    ((0, 1), (-1, 0)): utility.menu.load_image('body_tl', 1.6)
}
"""
Изображения тела.

Для получения изображения используются старое и новое направления.
"""


class sound_turn:
    def play_music(self):
        pass


class Wall(pg.sprite.Sprite):
    """
    Класс внутренней стены.

    :ivar image: Изображение стены.
    :type image: pg.Surface
    :ivar rect: Прямоугольник изображения.
    :type rect: pg.Rect

    """

    def __init__(self, x: int, y: int, group: pg.sprite.Group):
        super().__init__(group)
        self.image = tile_images['wall']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Key(pg.sprite.Sprite):
    """
    Класс ключа.

    :ivar image: Изображение ключа.
    :type image: pg.Surface
    :ivar rect: Прямоугольник изображения.
    :type rect: pg.Rect

    """

    def __init__(self, cur_space: list[tuple[int, int]], *groups: list[pg.sprite.Group]):
        super().__init__(*groups)
        self.image = tile_images['key']
        self.rect = self.image.get_rect()
        self.rect.topleft = cur_space[random.randint(0, len(cur_space) - 1)]

    def check_collision(self, snake) -> int:
        """
        Метод реакции на коллизию со змеёй.

        При коллизии удаляется из группы и удаляется из памяти.

        :param snake: Змея.
        :type snake: Snake

        :return: Получилось ли выполнить функцию.
        :rtype: int

        """
        snake.is_holding_key = True
        self.groups()[0].sprites()[0].image = tile_images['apple']
        self.groups()[0].remove(self)
        del self
        return 1


class Fruit(pg.sprite.Sprite):
    """
    Класс фрукта.

    :ivar counter_fruit: Номер фрукта. Нужен для определения того, когда стоит его делать особенным.
    :type counter_fruit: int
    :ivar empty_space: Множество ячеек, не являющихся стеной.
    :type empty_space: list[tuple[int, int]]
    :ivar image: Изображение фрукта.
    :type image: pg.Surface
    :ivar rect: Прямоугольник изображения.
    :type rect: pg.Rect
    :ivar is_special: Является ли фрукт особенным (под клеткой)
    :type is_special: bool

    """

    def __init__(self, counter_fruit: int, snake, empty_space: list[tuple[int, int]], group: pg.sprite.Group):
        super().__init__(group)
        self.counter_fruit = counter_fruit % fruit_step
        self.empty_space = empty_space
        cur_space = self.free_coords(snake, self.empty_space)

        self.image = tile_images['apple']
        self.rect = self.image.get_rect()
        self.rect.topleft = cur_space[random.randint(0, len(cur_space) - 1)]

        self.is_special = False

    def check_collision(self, snake) -> int:
        """
        Проверка коллизии со змеёй

        Если фрукт необычный И у змеи есть ключ ИЛИ фрукт обычный — update() + return 1
        В противном случае return -1

        :param snake: Змея.
        :type snake: Snake

        :return: Смогла ли змея взять фрукт.
        :rtype: int

        """
        if not self.is_special or self.is_special and snake.is_holding_key:
            snake.is_holding_key = False
            snake.len_queue += 1
            if self.is_special:
                snake.len_queue += 1
                global speed_movement
                speed_movement -= accel
                self.is_special = False
            self.update(snake)
            return 1
        return -1

    def free_coords(self, snake, space: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Определение ячеек без объектов.

        :param snake: Змея.
        :type snake: Snake
        :param space: Пространство без стен.
        :type space: list[tuple[int, int]]

        :return: Список координат ячеек без блоков змеи.
        :rtype: list[tuple[int, int]]

        """
        cur_space = space.copy()
        for body in snake.body:
            cur_space.remove(body.rect.topleft)

        if snake.prev_tail in cur_space:
            cur_space.remove(snake.prev_tail)

        plus_coords = (snake.body.sprites()[0].rect.topleft[0] + snake.cur_direction[0] * len_cell,
                       snake.body.sprites()[0].rect.topleft[1] + snake.cur_direction[1] * len_cell)
        if plus_coords in cur_space:
            cur_space.remove(plus_coords)
            """Реализовать убирание возможных координат добавления фрукта перед змеёй"""
            # issue: 46
        return cur_space

    def update(self, snake):
        """
        Изменение положение фрукта и, при необходимости, создание ключа.

        :param snake: Змея.
        :type snake: Snake

        """
        self.counter_fruit = (self.counter_fruit + 1) % fruit_step
        self.is_special = self.counter_fruit == 0 and len(self.empty_space) - 2 >= len(snake.body)

        cur_space = self.free_coords(snake, self.empty_space)

        coords = cur_space[random.randint(0, len(cur_space) - 1)]

        if not self.is_special:
            self.image = tile_images['apple']
            self.rect = self.image.get_rect()

        elif self.is_special:
            self.image = tile_images['apple_cage']
            self.rect = self.image.get_rect()
            cur_space.remove(coords)
            Key(cur_space, self.groups())

        self.rect.topleft = coords


class SnakeBody(pg.sprite.Sprite):
    """
    Класс блока тела змеи.

    :ivar image: Изображение блока тела.
    :type image: pg.Surface
    :ivar rect: Прямоугольник изображения.
    :type rect: pg.Rect
    :ivar dir: Текущее направление блока тела.

    """
    def __init__(self, x: int, y: int, image: pg.Surface, dir: tuple[int, int], group: pg.sprite.Group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.dir = dir

    def update(self, x: int, y: int, dir: tuple[int, int], image: pg.Surface) -> None:
        """
        Обновление блока тела.

        :param x: Координата блока тела по x.
        :type x: int
        :param y: Координата блока тела по y.
        :type y: int
        :param dir: Новое направление блока тела.
        :type dir: tuple[int, int]
        :param image: Изображение блока тела.
        :type image: pg.Surface

        """
        self.image = image
        self.rect = self.image.get_rect()
        self.dir = dir
        self.rect.topleft = (x, y)


class Snake:
    """
    Класс змеи.

    :ivar body_direction: Предыдущее направление змеи.
    :type body_direction: tuple[int, int]
    :ivar cur_direction: Текущее направление змеи. Также используется как направление для body[0] (головы).
    :type cur_direction: tuple[int, int]
    :ivar body: Положение множества блоков тела. В него не входит голова, но входит хвост.
    :type body: pg.sprite.Group
    :ivar is_holding_key: Держит ли змея ключ.
    :type is_holding_key: bool
    :ivar len_queue: Длина очереди на рост.
    :type len_queue: int
    :ivar prev_tail: Старые координаты хвоста. Нужны для правильной генерации нового фрукта.
    :type prev_tail: tuple[int, int]

    """

    def __init__(self, head_dir: tuple[int, int], head_pos: tuple[int, int], tail_pos: tuple[int, int]):
        self.cur_direction = head_dir
        self.body_direction = head_dir
        self.is_holding_key = False

        self.body = pg.sprite.Group()
        SnakeBody(*head_pos,
                  head_images[head_dir],
                  head_dir, self.body)
        SnakeBody(*tail_pos,
                  tail_images[head_dir[0], head_dir[1]],
                  head_dir, self.body)

        self.len_queue = 0
        """Длина очереди на рост"""
        self.prev_tail = (-1, -1)
        """координаты старого хвоста"""

    def add_block(self):
        """
        Добавление блока в змею.

        Хвост уходит назад.

        """
        SnakeBody(0, 0,
                  tail_images[(1, 0)], (0, 0), self.body)

    def draw_head(self):
        """
        Отрисовка головы при её повороте до движения.

        """
        image = self.image_head()
        coords = self.body.sprites()[0].rect.topleft
        self.body.sprites()[0].update(*coords, self.cur_direction, image)

    def image_head(self) -> pg.Surface:
        """
        Определение картинки для головы.

        :return: Картинка головы змеи.
        :rtype: pg.Surface

        """
        return head_images[self.cur_direction[0], self.cur_direction[1]]

    def draw(self, screen: pg.Surface):
        """
        Отрисовка тела змеи.

        :param screen: Экран, на котором будет отрисовано тело.
        :type screen: pg.Surface

        """
        self.body.draw(screen)

    def update(self, fruit_group: pg.sprite.Group, wall_group: pg.sprite.Group) -> bool:
        """
        Обновление спрайтов змеи.

        :param item_group: Группа предметов.
        :type item_group: pg.sprite.Group
        :param wall_group: Группа внутренних стен.
        :type wall_group: pg.sprite.Group

        :return: Как прошло обновление спрайтов.
        :rtype: bool

        """

        state_collision = self.is_collide(fruit_group, wall_group)
        if state_collision == -1:
            return False
        elif state_collision == 1:
            pass
            # play_sound_eating
            # self.add_block()
            # self.len_queue -= 1

        if self.len_queue != 0:
            self.add_block()
            self.len_queue -= 1

        prev_pos = self.body.sprites()[0].rect.topleft
        prev_dir = self.body_direction

        for index, block in enumerate(self.body):
            if index == 0:
                # Голова
                self.body_direction = self.cur_direction

                block.update(block.rect.x + self.cur_direction[0] * len_cell,
                             block.rect.y + self.cur_direction[1] * len_cell, self.cur_direction,
                             self.image_head())
                continue
            elif index == len(self.body) - 1:
                # Хвост
                self.prev_tail = block.rect.topleft
                pbd = self.body.sprites()[index - 1].dir
                block.update(*prev_pos, pbd, tail_images[pbd])
                continue

            # Тело
            to_set_pos = prev_pos
            to_set_dir = prev_dir
            prev_pos = block.rect.topleft
            prev_dir = block.dir
            block.update(*to_set_pos, to_set_dir,
                         body_images[to_set_dir, self.body.sprites()[index - 1].dir])

        return True

    def is_collide(self, item_group: pg.sprite.Group, wall_group: pg.sprite.Group) -> int:
        """
        Проверка змеи на предмет коллизии с различными объектами.

        Внешние стены проверяются по будущим координатам головы.

        :param item_group: Группа предметов.
        :type item_group: pg.sprite.Group
        :param wall_group: Группа внутренних стен.
        :type wall_group: pg.sprite.Group

        :return: Как прошла коллизия. 1 — фрукт, 0 — ничего, -1 — непроходимый объект.
        :rtype: int

        """
        future_head_coords = (self.body.sprites()[0].rect.topleft[0] + self.cur_direction[0] * len_cell,
                              self.body.sprites()[0].rect.topleft[1] + self.cur_direction[1] * len_cell)

        # Коллизия со внешними стенами
        if (0 > future_head_coords[0] or 0 > future_head_coords[1] or
                len_side_screen <= future_head_coords[0] or len_side_screen <= future_head_coords[1]):
            return -1

        # Коллизия со внутренними стенами
        for index_wall in range(len(wall_group)):
            wall_coords = wall_group.sprites()[index_wall].rect.topleft
            if future_head_coords == wall_coords:
                return -1

        # Коллизия с фруктом | ключем
        for item_index in range(len(item_group)):
            fruit_key_coords = item_group.sprites()[item_index].rect.topleft
            if future_head_coords == fruit_key_coords:
                return item_group.sprites()[item_index].check_collision(self)

        # Коллизия с телом
        for index in range(2, len(self.body) - 1):
            if future_head_coords == self.body.sprites()[index].rect.topleft:
                return -1
        # Коллизия с хвостом
        if future_head_coords == self.body.sprites()[-1].rect.topleft and self.len_queue > 0:
            return -1

        # Пустое пространство
        return 0

    def set_direction(self, direction: tuple[int, int]) -> bool:
        """
        Установка направления движения змеи.

        Если движение легально, то змея перерисовывается.

        :param direction: Пользовательское направление.
        :type direction: tuple[int, int]
        :return: Получилось ли изменить направление
        :rtype: bool

        """
        if self.body_direction == direction:
            self.cur_direction = direction
            return True
        elif self.body_direction[0] == -direction[0] and self.body_direction[1] == direction[1] or \
                self.body_direction[1] == -direction[1] and self.body_direction[0] == direction[0]:
            return False
        self.cur_direction = direction
        return True


class Game:
    """
    Класс игры.

    :ivar screen: Экран.
    :type screen: pg.Surface
    :ivar empty_space: Координаты пустых квадратов.
    :type empty_space: list[tuple[int, int]]
    :ivar walls_group: Группа внутренних стен.
    :type walls_group: pg.sprite.Group
    :ivar item_group: Группа предметов.
    :type item_group: pg.sprite.Group
    :ivar exit_pos: Координаты точки, врезавшись в стену рядом с которой уровень закончится. (НА БУДУЩЕЕ)
    :type exit_pos: tuple[int, int]
    :ivar snake: Змея.
    :type snake: Snake

    """
    def __init__(self, screen: pg.Surface, empty_space: list[tuple[int, int]], walls_coords: list[tuple[int, int]],
                 head_snake_pos: tuple[int, int], tail_snake_pos: tuple[int, int], exit_pos: tuple[int, int]):
        self.exit_pos = exit_pos
        self.screen = screen
        self.empty_space = empty_space

        self.walls_group = pg.sprite.Group()

        for wall_coords in walls_coords:
            Wall(*wall_coords, self.walls_group)

        snake_dir = (1, 0)

        if head_snake_pos[0] == tail_snake_pos[0]:
            # Находятся на одной OX
            if head_snake_pos[1] > tail_snake_pos[1]:
                snake_dir = (0, 1)
            else:
                snake_dir = (0, -1)
        elif head_snake_pos[1] == tail_snake_pos[1]:
            # Находятся на одной OY
            if head_snake_pos[0] > tail_snake_pos[0]:
                snake_dir = (1, 0)
            else:
                snake_dir = (-1, 0)

        self.snake = Snake(snake_dir, head_snake_pos, tail_snake_pos)

        self.item_group = pg.sprite.Group()
        Fruit(1, self.snake, self.empty_space, self.item_group)

    def game_loop(self) -> int:
        """
        Игровой цикл.

        :return: Длина змеи.
        :rtype int:
        """
        move_snake_event = pg.USEREVENT + 1
        gameover_event = pg.USEREVENT + 2

        self.draw_level()
        pg.time.set_timer(move_snake_event, speed_movement)  # скорость такта движения змеи.

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    utility.menu.menu_index = -1
                if event.type == gameover_event:
                    running = False
                    continue
                if event.type == move_snake_event:
                    running = self.snake.update(self.item_group, self.walls_group)  # Обновление положения змеи
                    if not running:
                        utility.menu.menu_index = 2
                        break
                    self.draw_level()
                    pg.time.set_timer(move_snake_event, speed_movement)  # Обновление скорости змеи
                if event.type == pg.KEYDOWN:
                    # Попытка обновления направления змеи
                    # Звук по остатку от деления счётчика звука на кол-во звуков.
                    state = False
                    if event.key == pg.K_UP:
                        state = self.snake.set_direction((0, -1))
                    elif event.key == pg.K_DOWN:
                        state = self.snake.set_direction((0, 1))
                    elif event.key == pg.K_LEFT:
                        state = self.snake.set_direction((-1, 0))
                    elif event.key == pg.K_RIGHT:
                        state = self.snake.set_direction((1, 0))
                    if state:
                        self.snake.draw_head()
                        self.draw_level()
        return len(self.snake.body) - 2

    def draw_level(self):
        """
        Отрисовка уровня.

        """
        self.screen.fill('black')
        utility.menu.background_render(self.screen, len_side_screen, count_cells)
        self.walls_group.draw(self.screen)
        self.snake.draw(self.screen)
        self.item_group.draw(self.screen)
        pg.display.flip()
        # pg.display.flip()
