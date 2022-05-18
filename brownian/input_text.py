from brownian.gui_component import GUIComponent
import pygame

from brownian.text import Text

class InputText(GUIComponent):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.active = False

        self.pos = (pos_x, pos_y)

        self.text = Text("", (0, 0, 0))
        self.set_text()

    def set_text(self):
        text_width, text_height = self.text.text_rendered.get_size()

        margin_x = self.rect.x + (self.rect.width - text_width) // 2
        margin_y = self.rect.y + (self.rect.height - text_height) // 2

        self.text.set_pos(margin_x, margin_y)

    def click(self):
        if self.rect.collidepoint(self.mouse):
            self.active = not self.active
        else:
            self.active = False

    def update(self):
        self.text.update()
        self.set_text()
        self.mouse = pygame.mouse.get_pos()

        if self.active:
            self.image.fill((255, 255, 255))
        else:
            self.image.fill((210, 210, 210))

        if self.rect.left <= self.mouse[0] <= self.rect.right and self.rect.top <= self.mouse[1] <= self.rect.bottom:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text.text = self.text.text[:-1]
                else:
                    self.text.text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.text.draw(screen)

    def get_text(self):
        return self.text.text


    
