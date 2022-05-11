import pygame

class Text:
    def __init__(self, text, color, hover_color=None, font_name="Corbel", font_size=20, pos_x=0, pos_y=0):
        self.color = color
        self.hover_color = color if not hover_color else hover_color

        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = text
        self.text_rendered = self.font.render(text, True, color)

        self.pos = (pos_x, pos_y)

    def draw(self, screen):
        screen.blit(self.text_rendered, self.pos)
        
