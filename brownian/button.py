import pygame
from text import Text
class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, text, color=(80, 80, 80), hover_color=(35, 35, 35)):
        super().__init__()

        self.color = color
        self.hover_color = hover_color

        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.text = text

    def update(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.left <= mouse[0] <= self.rect.right and self.rect.top <= mouse[1] <= self.rect.bottom:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image.fill(self.hover_color)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.image.fill(self.color)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.text.draw(screen)

    