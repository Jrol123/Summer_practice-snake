"""
Empty.
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
speed_movement = int(config['game']['speed'])
len_cell = len_side_screen // count_cells

tile_images = {
    'wall': utility.menu.load_image('wall-block(r)', 2),
    'apple': utility.menu.load_image('apple', 2),
    'cage': utility.menu.load_image('cage', 2)
}


class sound_turn:
    def play_music(self):
        pass


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = tile_images['wall']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


"""
У змеи будет параметр is_holding_key, отвечающий за возможность взять "особенный" фрукт
"""

"""
Ключ будет лежать в одной группе с Fruit
"""


class Fruit(pg.sprite.Sprite):
    def __init__(self, counter_fruit, empty_space, group):
        super().__init__(group)
        self.counter_fruit = counter_fruit % 5
        # Сделать двойной цикл, где для каждого snake_obj проверяется empty_space. Если есть коллизия — удаляется
        self.x, self.y = empty_space[random.randint(0, len(empty_space) - 1)]
        # Исключить координаты змеи.
        # Исключить координату перед змеёй.

        self.image = tile_images['apple']
        self.rect = pg.Rect(self.x, self.y, len_cell, len_cell)
        self.is_special = False
        """Является ли фрукт - особенным (под клеткой)"""

    def check_collision(self, snake) -> int:
        """
        Если у змеи есть ключ ИЛИ фрукт обычный — update() + return 1
        В противном случае return -1
        :type snake: Snake
        :return:

        """
        if not self.is_special or self.is_special and snake.is_holding_key:
            self.update()
            snake.len_queue += 1 + int(self.is_special)
            return 1
        return -1

    # def update(self, snake):
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
2. Как работать с анимациями в данной игре?
И нужны ли они вообще?
Скорее всего нет, потому как я их вообще не успею добавить, что, конечно, печально.

3. Как определять коллизии с предметом?
Через класс змеи?

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
    def __init__(self, x, y, image, dir, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.dir = dir

    def update(self, x: int, y: int, dir: tuple[int, int], image=None) -> None:
        if image != None:
            self.image = image
            self.rect = self.image.get_rect()
        self.dir = dir
        self.rect.topleft = (x, y)


class Snake:
    """
    Класс змеи.

    :ivar body_direction: Предыдущее направление змеи
    :type body_direction: tuple[int, int]
    :ivar cur_direction: Текущее направление змеи. Также используется как направление для body[0] (головы)
    :type cur_direction: tuple[int, int]
    :ivar body: Положение множества блоков тела. В него не входит голова, но входит хвост

    """

    def __init__(self, head_dir: tuple[int, int], head_pos: tuple[int, int], tail_pos: tuple[int, int]):
        self.cur_direction = head_dir
        self.body_direction = head_dir
        self.is_holding_key = False
        # self.head = utility.menu.load_image('head_right', 2)

        self.head_images = {
            (1, 0): utility.menu.load_image('head_right', 1.6),
            (-1, 0): utility.menu.load_image('head_left', 1.6),
            (0, -1): utility.menu.load_image('head_up', 1.6),
            (0, 1): utility.menu.load_image('head_down', 1.6)
        }
        # Для отображения хвоста берётся только направление его "предыдущего" блока
        self.tail_images = {
            (-1, 0): utility.menu.load_image('tail_right', 1.6),
            (1, 0): utility.menu.load_image('tail_left', 1.6),
            (0, 1): utility.menu.load_image('tail_up', 1.6),
            (0, -1): utility.menu.load_image('tail_down', 1.6)
        }
        self.body_images = {
            ((1, 0), (1, 0)): utility.menu.load_image('body_horizontal', 1.6),
            ((-1, 0), (-1, 0)): utility.menu.load_image('body_horizontal', 1.6),
            ((0, 1), (0, 1)): utility.menu.load_image('body_vertical', 1.6),
            ((0, -1), (0, -1)): utility.menu.load_image('body_vertical', 1.6),
            ((0, -1), (1, 0)): utility.menu.load_image('body_br', 1.6),
            ((-1, 0), (1, 0)): utility.menu.load_image('body_br', 1.6),
            ((1, 0), (0, 1)): utility.menu.load_image('body_bl', 1.6),
            ((0, -1), (-1, 0)): utility.menu.load_image('body_bl', 1.6),
            ((0, 1), (1, 0)): utility.menu.load_image('body_tr', 1.6),
            ((-1, 0), (0, -1)): utility.menu.load_image('body_tr', 1.6),
            ((1, 0), (0, -1)): utility.menu.load_image('body_tl', 1.6),
            ((0, 1), (-1, 0)): utility.menu.load_image('body_tl', 1.6)
        }

        self.body = pg.sprite.Group()
        SnakeBody(*head_pos,
                  self.head_images[head_dir],
                  head_dir, self.body)
        SnakeBody(*tail_pos,
                  self.tail_images[head_dir[0], head_dir[1]],
                  head_dir, self.body)

        self.prev_pos = (tail_pos[0] - 1, tail_pos[1] - 1)
        """Информация о предыдущей последней клетке для корректного отрисовывания хвоста"""

        self.len_queue = 0
        """Длина очереди на рост"""

    def add_block_to_snake(self):
        pass

    def image_head(self) -> pg.Surface:
        return self.head_images[self.cur_direction[0], self.cur_direction[1]]

    def draw(self, screen):
        self.body.draw(screen)

    def update(self, fruit_group, wall_group) -> bool:
        """
        Обновление спрайтов змеи.

        """
        # Работать с направлениями блоков.
        # Если блок не первый, то мы смотрим, куда он ушёл.
        # Если движение следующего блока не изменилось (он не ушёл с предыдущей прямой) спрайт не обновляется.
        # В противном случае смотрим на старое направление и на новое направление

        # 1. Сохранять коорды переднего блока до изменения -> Перемещать текущий блок на место нового
        # 2. Брать текстуру исходя из текущего направления + направления "предыдущего" блока
        # 3. Менять направление.
        if self.len_queue != 0:
            self.add_block()

        prev_block_pos = self.body.sprites()[0].rect.topleft

        for index, block in enumerate(self.body):
            if index == 0:
                # Голова
                state_collision = self.is_collide(fruit_group, wall_group)
                # -1 — врезался в непроходимый объект.
                # 1 — фрукт
                # 0 — ничего
                if state_collision == -1:
                    return False

                self.body_direction = self.cur_direction

                block.update(block.rect.x + self.cur_direction[0] * len_cell,
                             block.rect.y + self.cur_direction[1] * len_cell, self.cur_direction,
                             self.image_head())
                continue
            elif index == len(self.body) - 1:
                # Хвост
                prev_block_dir = self.body.sprites()[index - 1].dir
                block.update(*prev_block_pos, prev_block_dir, self.tail_images[prev_block_dir])
                continue

            prev_block_dir = self.body.sprites()[index - 1].dir
            to_set_pos = prev_block_pos
            prev_block_pos = block.rect.topleft
            block.update(*to_set_pos, prev_block_dir, self.body_images[block.dir, prev_block_dir])

        return True

    def is_collide(self, fruit_group: pg.sprite.Group, wall_group) -> int:
        """
        Проверка змеи на предмет коллизии.

        Внешние стены проверяются по-координатам.
        Внутренни

        """
        future_head_coords = (self.body.sprites()[0].rect.topleft[0] + self.cur_direction[0] * len_cell,
                              self.body.sprites()[0].rect.topleft[1] + self.cur_direction[1] * len_cell)
        # Коллизия со внешними стенами
        if (0 > future_head_coords[0] or 0 > future_head_coords[1] or
                len_side_screen < future_head_coords[0] or len_side_screen < future_head_coords[1]):
            return -1

        # Коллизия со внутренними стенами
        for index_wall in range(len(wall_group)):
            wall_coords = wall_group.sprites()[index_wall].rect.topleft
            if future_head_coords == wall_coords:
                return -1

        # Коллизия со фруктом | ключем
        for index_fruit_key in range(len(fruit_group)):
            fruit_key = fruit_group.sprites()[index_fruit_key].rect.topleft
            if future_head_coords == fruit_key:
                return fruit_group.sprites()[index_fruit_key].check_collision(self)

        # Пустое пространство
        return 0

    def add_block(self) -> None:
        """
        Добавление блока в змею

        Хвост уходит назад

        """

    def set_direction(self, direction) -> bool:
        """
        Установка направления движения змеи.

        Если движение легально, то змея тут-же отрисовывается.

        :param direction: Пользовательское направление.
        :return: Получилось ли изменить направление

        """
        if self.body_direction[0] == -direction[0] and self.body_direction[1] == direction[1] or \
                self.body_direction[1] == -direction[1] and self.body_direction[0] == direction[0]:
            return False
        self.cur_direction = direction
        return True


class Game:
    def __init__(self, screen: pg.Surface, empty_space, walls, head_snake, tail_snake, exit_pos, level):
        """

        :param screen: Экран
        :param empty_space: Координаты пустых квадратов
        :param walls: Координаты стен
        :param head_snake: Координаты головы змеи
        :param tail_snake: Координаты хвоста змеи
        :param exit_pos: Координаты точки, врезавшись в стену рядом с которой уровень закончится (НА БУДУЩЕЕ)

        """
        self.level = level
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

    def game_loop(self) -> int:
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
                    running = self.snake.update(self.fruits_group, self.walls_group)  # Обновление положения змеи
                    if not running:
                        utility.menu.menu_index = 2
                        break
                    self.draw_level()
                if event.type == pg.KEYDOWN:
                    # Попытка обновления направления змеи
                    # pg.event.post(gameover_ev)
                    # Звук по-модулю
                    state = False
                    if event.key == pg.K_UP:
                        state = self.snake.set_direction((0, -1))
                    elif event.key == pg.K_DOWN:
                        state = self.snake.set_direction((0, 1))
                    elif event.key == pg.K_LEFT:
                        state = self.snake.set_direction((-1, 0))
                    elif event.key == pg.K_RIGHT:
                        state = self.snake.set_direction((1, 0))

                    # Условие, отвечающее за то, чтобы при успешном нажатии змея моментально меняла направление,
                    # не дожидаясь следующего такта
                    if state:
                        pg.event.post(pg.event.Event(move_snake_event))
                        pg.time.set_timer(move_snake_event, speed_movement)
        return len(self.snake.body) - 2

    def draw_level(self):
        self.screen.fill('black')
        utility.menu.background_render(self.screen, len_side_screen, count_cells)
        self.walls_group.draw(self.screen)
        self.snake.draw(self.screen)
        pg.display.flip()
        # self.fruits_group.draw(self.screen)
        # pg.display.flip()
