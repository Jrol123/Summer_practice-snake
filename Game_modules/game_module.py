"""
Empty.
"""
import configparser
from abc import abstractmethod
import pygame as pg
from pygame import Vector2
import utility.level_system
import utility.menu
import random

config = configparser.ConfigParser()
config.read('config.cfg')
len_side_screen = int(config['screen']['len_side'])
count_cells = int(config['screen']['count_cells'])
speed_movement = int(config['game']['speed'])
len_cell = len_side_screen // count_cells

tile_images = {
    'wall': utility.menu.load_image('wall-block(r)', 2),
    'apple': utility.menu.load_image('apple', 2),
    'cage': utility.menu.load_image('cage', 2)
}


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = tile_images['wall']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        print(x, y)


"""
Можно или каждый раз отрисовывать новый фрукт, или просто переносить старый и менять его параметры.
Соответственно, если фрукт станет "особенным", то генерировать ключ.
ИЛИ можно сделать счётчик, чтобы каждый 5-й фрукт был "особенным".
"""
"""
У змеи будет параметр is_holding_key, отвечающий за возможность взять "особенный" фрукт
"""


class Fruit(pg.sprite.Sprite):
    def __init__(self, counter_fruit, group):
        super().__init__(group)
        self.counter_fruit = counter_fruit % 5
        self.x = random.randint(0, len(Game().empty_space) - 1)
        self.y = random.randint(0, len(Game().empty_space) - 1)
        # Исключить координаты змеи

        self.rect = pg.Rect(self.x, self.y, len_cell, len_cell)
        self.is_special = False

    # def update(self):
    #     """
    #     Как можно связать коллизию с анимацией?
    #
    #     """
    #     # if Snake.head.pos == (self.x, self.y): # Просто сравнение
    #     if is_collided_by_snake:
    #         if (self.is_special and Snake.is_holding_key) or not self.is_special:
    #             Snake.queue_len += 1 + int(self.is_special)
    #             if not Snake.is_growing:
    #                 Snake.start_grow()  # Метод роста с сохранением
    #         elif self.is_special and not Snake.is_holding_key:
    #             Game_modules.gameover


"""
Будет хранить в себе блоки головы, тела и хвоста.
Каждый блок будет вектором (pg.Vector2)

Блок тела будет отрисовываться относительно положения следующего блока и предыдущего
(в крайнем случае — относительно головы и хвоста)

Или же можно сделать хвост частью тела
"""

"""
1. Как реализовать сам процесс игры?
Через абстрактный класс?

2. Как работать с анимациями в данной игре?
И нужны ли они вообще?
Скорее всего нет, потому как я их вообще не успею добавить, что, конечно, печально.

3. Как определять коллизии с предметом?

4. Как отрисовывать змею?
С учётом того, что она движется...
Следует ли создать класс под тело змеи и просто отрисовывать спрайтами, или же работать через blit ?

5. Как отрисовывать фрукты?
Если учесть, что фрукты не могут появляться прямо на змее или перед змеёй

6. Как учитывать то, что хвост должен оставаться на месте?
Всегда хранить его предыдущие координаты и в случае чего откатывать хвост на них, чтобы при продвижении далее хвост снова подвинулся на своё исходное место?

"""


class Snake:
    """
    Класс змеи.

    :ivar direction: Направление змеи
    :type direction: Vector2
    :ivar body: Положение множества блоков тела. В него не входит голова, но входит хвост

    """

    def __init__(self, head_dir, pos_tail):
        self.cur_direction = Vector2(*head_dir)
        self.body_direction = self.cur_direction.copy()
        self.head = utility.menu.load_image('head_right')

        self.head_up = utility.menu.load_image('head_up')
        self.head_down = utility.menu.load_image('head_down')
        self.head_right = utility.menu.load_image('head_right')
        self.head_left = utility.menu.load_image('head_left')

        self.body = [Vector2(*pos_tail)]

        self.tail_up = utility.menu.load_image('tail_up')
        self.tail_down = utility.menu.load_image('tail_down')
        self.tail_right = utility.menu.load_image('tail_right')
        self.tail_left = utility.menu.load_image('tail_left')

        self.body_vertical = utility.menu.load_image('body_vertical')
        self.body_horizontal = utility.menu.load_image('body_horizontal')

        self.body_tr = utility.menu.load_image('body_tr')
        self.body_tl = utility.menu.load_image('body_tl')
        self.body_br = utility.menu.load_image('body_br')
        self.body_bl = utility.menu.load_image('body_bl')

        self.prev_pos = Vector2(pos_tail[0] - 1, pos_tail[1] - 1)
        """Информация о предыдущей последней клетке для корректного отрисовывания хвоста"""

    def add_block_to_snake(self):
        pass

    def draw_head(self):
        if self.cur_direction == (1, 0):
            self.head = self.head_right
        if self.cur_direction == (-1, 0):
            self.head = self.head_left
        if self.cur_direction == (0, -1):
            self.head = self.head_up
        if self.cur_direction == (0, 1):
            self.head = self.head_down

    def move_snake(self):
        body_double = self.body[:-1]
        body_double.insert(0, body_double[0] + self.cur_direction)
        self.body_direction = self.cur_direction
        self.body = body_double[:]

    def set_direction(self, direction):
        if self.body_direction[0] == -direction[0] and self.body_direction[1] == direction[1]:
            return
        self.cur_direction = direction


class Game:
    @abstractmethod
    def start(self, screen: pg.Surface, empty_space, walls, head_snake, tail_snake, exit_pos):
        """

        :param screen: Экран
        :param empty_space: Координаты пустых квадратов
        :param walls: Координаты стен
        :param head_snake: Координаты головы змеи
        :param tail_snake: Координаты хвоста змеи
        :param exit_pos: Координаты точки, врезавшись в стену рядом с которой уровень закончится (НА БУДУЩЕЕ)

        """
        self.exit_pos = exit_pos
        self.screen = screen
        self.empty_space = empty_space
        self.fruits_group = pg.sprite.Group()
        self.fruit = Fruit(1, self.fruits_group)

        self.walls_group = pg.sprite.Group()

        for wall_coords in walls:
            Wall(*wall_coords, self.walls_group)

        snake_dir = Vector2(1, 0)

        if head_snake[0] == tail_snake[0]:
            # Находятся на одной OX
            if head_snake[1] > tail_snake[1]:
                snake_dir = Vector2(1, 0)
            else:
                snake_dir = Vector2(-1, 0)
        elif head_snake[1] == tail_snake[1]:
            # Находятся на одной OY
            if head_snake[0] > tail_snake[0]:
                snake_dir = Vector2(0, 1)
            else:
                snake_dir = Vector2(0, -1)

        self.snake = Snake(snake_dir, tail_snake)

        self.game_loop()

    def game_loop(self):
        move_snake_event = pg.USEREVENT

        self.draw_level()
        pg.time.set_timer(move_snake_event, speed_movement)  # скорость обработки движения змеи

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    utility.menu.menu_index = -1
                if event.type == move_snake_event:
                    self.snake.update()  # Обновление положения змеи
                if event.type == pg.KEYDOWN:
                    # Попытка обновления направления змеи
                    if event.key == pg.K_UP:
                        self.snake.set_direction(Vector2(0, -1))
                    elif event.key == pg.K_DOWN:
                        self.snake.set_direction(Vector2(0, 1))
                    elif event.key == pg.K_LEFT:
                        self.snake.set_direction(Vector2(-1, 0))
                    elif event.key == pg.K_RIGHT:
                        self.snake.set_direction(Vector2(1, 0))
                self.draw_level()
                self.snake.draw(self.screen)
                self.fruits_group.draw(self.screen)

    def draw_level(self):
        self.screen.fill('black')
        utility.menu.background_render(self.screen, len_side_screen, count_cells)
        self.walls_group.draw(self.screen)
        pg.display.flip()

    def gameover(self):
        utility.menu.gameover_screen(self.screen, len_side_screen, count_cells, len(self.snake.body) - 1)
