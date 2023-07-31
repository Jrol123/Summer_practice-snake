"""
Здесь будут содержаться коды ко всем меню (см. Milestone Механики)
"""
import pygame
from utility.field import Board


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

    def update(self, mouse_pos, *args) -> int | None:
        if self.rect.collidepoint(mouse_pos):
            return self.action(args)


def background_render(screen: pygame.Surface, len_side_screen: int, count_cells: int) -> None:
    bgrd = Board(len_side_screen, count_cells)
    bgrd.draw(screen)


def start_screen(screen: pygame.Surface, len_side_screen: int, count_cells: int) -> None:
    """
    Начальный экран.

    """
    background_render(screen, len_side_screen, count_cells)

    intro_text = ["Snake 2.0"]
    font = pygame.font.Font(None, 100)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('violet'))
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


def gameover_screen(screen: pygame.Surface, len_side_screen: int, count_cells: int, len_snake: int) -> None:
    pass
