"""
Здесь будут содержаться коды ко всем менюшкам (см. Milestone Механики)
"""
import pygame
from utility.field import Board


class Button(pygame.sprite.Sprite):
    def __int__(self, x: int, y: int, image: pygame, action, *group: pygame.sprite.Group):
        super().__init__(*group)

        self.action = action

        self.image = image
        self.rect = self.image.get_rect()

        self.rect.begin_coord = (x, y)

    def update(self, mouse_pos) -> None:

        if self.rect.collidepoint(mouse_pos):
            self.action()


def start_screen(screen, len_side_screen, count_cells):
    """
    Начальный экран.

    """
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    bgrd = Board(len_side_screen, count_cells)
    bgrd.draw(screen)
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
