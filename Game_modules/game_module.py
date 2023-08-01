"""
Empty.
"""
import configparser
from abc import abstractmethod
import pygame as pg
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


"""
У змеи будет параметр is_holding_key, отвечающий за возможность взять "особенный" фрукт
"""


class Fruit(pg.sprite.Sprite):
    def __init__(self, counter_fruit, empty_space, group):
        super().__init__(group)
        self.counter_fruit = counter_fruit % 5
        self.x = random.randint(0, len(empty_space) - 1)
        self.y = random.randint(0, len(empty_space) - 1)
        # Исключить координаты змеи

        self.rect = pg.Rect(self.x, self.y, len_cell, len_cell)
        self.is_special = False
        """Является ли фрукт - особенным (под клеткой)"""

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
"""
1. При нажатии на кнопки таймер тут-же сбрасывается и змея моментально двигается.
В противном случае происходит таймер и змея двигается по-направлению

2. snake.body будет содержать ВСЕ элементы тела, в том числе и голову с хвостом.
В случае необходимости они просто будут обновляться и всё.
Направление движения будет храниться в отдельной переменной.
"""


class SnakeBody(pg.sprite.Sprite):
    def __init__(self, x, y, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, x: int, y: int, image=None) -> None:
        if image != None:
            self.image = image
            self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Snake:
    """
    Класс змеи.

    :ivar body_direction: Предыдущее направление змеи
    :type body_direction: Vector2
    :ivar cur_direction: Текущее направление змеи
    :type cur_direction: Vector2
    :ivar body: Положение множества блоков тела. В него не входит голова, но входит хвост

    """

    def __init__(self, head_dir, head_pos, tail_pos):
        self.cur_direction = head_dir
        self.body_direction = head_dir
        # self.head = utility.menu.load_image('head_right', 2)

        self.head_images = {
            (1, 0): utility.menu.load_image('head_right', 1.6),
            (-1, 0): utility.menu.load_image('head_left', 1.6),
            (0, -1): utility.menu.load_image('head_up', 1.6),
            (0, 1): utility.menu.load_image('head_down', 1.6)
        }
        self.tail_images = {
            (1, 0): utility.menu.load_image('tail_right', 1.6),
            (-1, 0): utility.menu.load_image('tail_left', 1.6),
            (0, -1): utility.menu.load_image('tail_up', 1.6),
            (0, 1): utility.menu.load_image('tail_down', 1.6)
        }

        self.body = pg.sprite.Group()
        SnakeBody(*head_pos, self.head_images[head_dir], self.body)
        SnakeBody(*tail_pos, self.tail_images[-head_dir[0], -head_dir[1]], self.body)  # Умножение на -1 происходит из-за особенностей текстур

        self.body_vertical = utility.menu.load_image('body_vertical', 1.6)
        self.body_horizontal = utility.menu.load_image('body_horizontal', 1.6)

        self.body_tr = utility.menu.load_image('body_tr', 1.6)
        self.body_tl = utility.menu.load_image('body_tl', 1.6)
        self.body_br = utility.menu.load_image('body_br', 1.6)
        self.body_bl = utility.menu.load_image('body_bl', 1.6)

        self.prev_pos = (tail_pos[0] - 1, tail_pos[1] - 1)
        """Информация о предыдущей последней клетке для корректного отрисовывания хвоста"""

    def add_block_to_snake(self):
        pass

    def draw_head(self):
        return self.head_images[self.cur_direction[0], self.cur_direction[1]]

    def draw(self, screen):
        self.body.draw(screen)

    def draw_body(self):
        pass

    def move_snake(self):
        body_double = self.body[:-1]
        body_double.insert(0, body_double[0] + self.cur_direction)
        self.body_direction = self.cur_direction
        self.body = body_double[:]

    def set_direction(self, direction) -> bool:
        if self.body_direction[0] == -direction[0] and self.body_direction[1] == direction[1]:
            return False
        self.cur_direction = direction
        return True


class Game:
    def __init__(self, screen: pg.Surface, empty_space, walls, head_snake, tail_snake, exit_pos):
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
        self.fruit = Fruit(1, self.empty_space, self.fruits_group)

        self.walls_group = pg.sprite.Group()

        for wall_coords in walls:
            Wall(*wall_coords, self.walls_group)

        snake_dir = (1, 0)

        if head_snake[0] == tail_snake[0]:
            # Находятся на одной OX
            if head_snake[1] > tail_snake[1]:
                snake_dir = (0, 1)
            else:
                snake_dir = (0, -1)
        elif head_snake[1] == tail_snake[1]:
            # Находятся на одной OY
            if head_snake[0] > tail_snake[0]:
                snake_dir = (1, 0)
            else:
                snake_dir = (-1, 0)

        self.snake = Snake(snake_dir, head_snake, tail_snake)

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
                    # self.snake.update()  # Обновление положения змеи
                    self.draw_level()
                if event.type == pg.KEYDOWN:
                    # Попытка обновления направления змеи
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
                        self.snake.update()
                        pg.time.set_timer(move_snake_event, speed_movement)
                self.draw_level()
                # self.snake.draw(self.screen)
                # pg.display.flip()
                # self.fruits_group.draw(self.screen)

    def draw_level(self):
        self.screen.fill('black')
        utility.menu.background_render(self.screen, len_side_screen, count_cells)
        self.walls_group.draw(self.screen)
        self.snake.draw(self.screen)
        pg.display.flip()
        # self.fruits_group.draw(self.screen)
        # pg.display.flip()

    def gameover(self):
        utility.menu.gameover_screen(self.screen, len_side_screen, count_cells, len(self.snake.body) - 1)
