from brownian.gui_component import GUIComponent
import pygame

class CheckBox(GUIComponent):
    def __init__(self, pos_x, pos_y, radius):
        super().__init__()

        self.radius = radius
        self.pos = (pos_x, pos_y)

        self.checked = False

        self.rect = pygame.Rect(pos_x-radius, pos_y-radius, radius * 2, radius * 2)
        self.list_to_unchecked = list()

    def set_list_to_unchecked(self, list_unchecked):
        self.list_to_unchecked = list_unchecked

    def update(self):
        self.mouse = pygame.mouse.get_pos()

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.pos, self.radius)

        if self.checked:
            pygame.draw.circle(screen, (0, 0, 0), self.pos, self.radius // 2)

    def click(self):
        if self.rect.collidepoint(self.mouse):
            self.checked = not self.checked

            for elemenent in self.list_to_unchecked:
                elemenent.checked = not elemenent.checked