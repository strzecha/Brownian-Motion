from brownian.input_text import InputText
from brownian.text import Text
from brownian.button import Button
from brownian.simulation import Simulation
from brownian.label import Label
from brownian.check_box import CheckBox

import pygame

class Window:
    def __init__(self, screen_width, screen_height, fill_color):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = pygame.display.set_mode((screen_width, screen_height))

        self.gui_components = pygame.sprite.Group()

        self.fill_color = fill_color

        way_label = Label("SPOSÓB SYMULACJI:", pos_x=310, pos_y=20)
        self.add_component(way_label)

        wiener_label = Label("Cykl Wienera", pos_x=225, pos_y=70)
        self.add_component(wiener_label)

        self.wiener_checkbox = CheckBox(pos_x=347, pos_y=77, radius=10)
    
        self.add_component(self.wiener_checkbox)

        physics_label = Label("Odbijanie cząsteczek", pos_x=375, pos_y=70)
        self.add_component(physics_label)

        self.physics_checkbox = CheckBox(pos_x=560, pos_y=77, radius=10)
        self.physics_checkbox.set_list_to_unchecked([self.wiener_checkbox])
        self.add_component(self.physics_checkbox)

        self.wiener_checkbox.set_list_to_unchecked([self.physics_checkbox])

        start_text = Text("Start", (0, 0, 0), pos_x = 400, pos_y=105)
    
        self.start_but = Button(200, 50, 300, 600, start_text, self.start_simulation, (100, 100, 100), (80, 80, 80))
        self.add_component(self.start_but)

        way_label = Label("CZĄSTECZKI CIECZY:", pos_x=310, pos_y=125)
        self.add_component(way_label)

        num_particles_label = Label("Liczba cząsteczek", pos_x=250, pos_y=155)
        self.add_component(num_particles_label)

        self.particles_input = InputText(200, 30, 400, 150)
        self.add_component(self.particles_input)

        radius_particles_label = Label("Promień cząsteczek", pos_x=230, pos_y=205)
        self.add_component(radius_particles_label)

        self.radius_particles_input = InputText(200, 30, 400, 200)
        self.add_component(self.radius_particles_input)

    def start_simulation(self):
        num_of_particles = int(self.particles_input.get_text())
        use_wiener = self.wiener_checkbox.checked

        sim = Simulation(self.window, num_of_particles, 1, use_wiener=use_wiener)

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

                for component in self.gui_components:
                            component.handle_event(event)

            # if pygame.mouse.get_pressed()[0]:
            #         for component in self.gui_components:
            #             component.click()

            self.fill()
            self.draw()
            self.update()

