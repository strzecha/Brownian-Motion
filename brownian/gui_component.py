import pygame

class GUIComponent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click()

    def click(self):
        pass
