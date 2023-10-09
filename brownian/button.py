import pygame

from brownian.gui_component import GUIComponent

class Button(GUIComponent):
    def __init__(self, width, height, pos_x, pos_y, text, action, color=(80, 80, 80), hover_color=(35, 35, 35)):
        super().__init__()

        self.color = color
        self.hover_color = hover_color

        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.action = action

        self.set_text(text)

    def set_text(self, text):
        self.text = text
        text_width, text_height = text.text_rendered.get_size()

        margin_x = self.rect.x + (self.rect.width - text_width) // 2
        margin_y = self.rect.y + (self.rect.height - text_height) // 2

        text.set_pos(margin_x, margin_y)

    def update(self):
        self.mouse = pygame.mouse.get_pos()

        if self.rect.left <= self.mouse[0] <= self.rect.right and self.rect.top <= self.mouse[1] <= self.rect.bottom:
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.color)

    def click(self):
        if self.rect.collidepoint(self.mouse):
            self.action()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.text.draw(screen)
 