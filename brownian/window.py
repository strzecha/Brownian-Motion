import pygame

class Window:
    def __init__(self, screen_width, screen_height, fill_color, gui_color):
        self.screen_width = screen_width
        self.gui_width = 200
        self.window = pygame.display.set_mode((screen_width+self.gui_width, screen_height))
        self.screen = pygame.Surface((screen_width, screen_height))
        self.screen_rect = self.screen.get_rect()

        self.gui = pygame.Surface((self.gui_width, screen_height))
        self.gui_rect = self.gui.get_rect()
        self.gui_rect.x = screen_width

        self.gui_components = pygame.sprite.Group()

        self.fill_color = fill_color
        self.gui_color = gui_color

    def add_component(self, component):
        self.gui_components.add(component)

    def update(self):
        self.gui_components.update()
        pygame.display.update()

    def draw(self):
        self.window.fill(self.fill_color, self.screen_rect)
        self.window.fill(self.gui_color, self.gui_rect)
        for component in self.gui_components:
            component.draw(self.window)
