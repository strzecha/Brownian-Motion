from brownian.text import Text
from brownian.button import Button
from brownian.simulation import Simulation
import pygame

class Window:
    def __init__(self, screen_width, screen_height, fill_color):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = pygame.display.set_mode((screen_width, screen_height))

        self.gui_components = pygame.sprite.Group()

        self.fill_color = fill_color

        start_text = Text("Start", (0, 0, 0), pos_x = 400, pos_y=105)
    
        start_but = Button(200, 50, 300, 600, start_text, self.start_simulation, (100, 100, 100), (80, 80, 80))
        self.add_component(start_but)

    def start_simulation(self):
        sim = Simulation(self.window, 20, 1)

        sim.simulate()

    def add_component(self, component):
        self.gui_components.add(component)

    def update(self):
        self.gui_components.update()   
        pygame.display.update()
        

    def fill(self):
        self.window.fill(self.fill_color)

    def draw(self):
        for component in self.gui_components:
            component.draw(self.window)

    def start(self):
        go = True

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go = False
            if pygame.mouse.get_pressed()[0]:
                    for component in self.gui_components:
                        component.click()

            self.fill()
            self.draw()
            self.update()

