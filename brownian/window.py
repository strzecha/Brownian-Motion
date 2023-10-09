import pygame

from brownian.input_text import InputText
from brownian.text import Text
from brownian.button import Button
from brownian.simulation import Simulation
from brownian.label import Label
from brownian.check_box import CheckBox

class Window:
    """Class Window

    Class to representation of window
    """

    def __init__(self, screen_width, screen_height, fill_color):
        """Init method

        Args:
            screen_width (int): width of window
            screen_height (int): height of window
            fill_color (tuple): color of window's background
        """

        pygame.init()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = pygame.display.set_mode((screen_width, screen_height))

        self.gui_components = pygame.sprite.Group()

        self.fill_color = fill_color

        way_label = Label("SPOSÓB SYMULACJI:", pos_x=210, pos_y=20)
        self.add_component(way_label)

        wiener_label = Label("Cykl Wienera", pos_x=125, pos_y=60)
        self.add_component(wiener_label)

        self.wiener_checkbox = CheckBox(pos_x=247, pos_y=67, radius=10)
        self.wiener_checkbox.checked = True
    
        self.add_component(self.wiener_checkbox)

        physics_label = Label("Odbijanie cząsteczek", pos_x=275, pos_y=60)
        self.add_component(physics_label)

        self.physics_checkbox = CheckBox(pos_x=460, pos_y=67, radius=10)
        self.physics_checkbox.set_list_to_unchecked([self.wiener_checkbox])
        self.add_component(self.physics_checkbox)

        self.wiener_checkbox.set_list_to_unchecked([self.physics_checkbox])

        way_label = Label("Czy chcesz rysować drogę odbijanych cząsteczek:", pos_x=70, pos_y=95)
        self.add_component(way_label)

        self.lines_checkbox = CheckBox(pos_x=480, pos_y=103, radius=10)
        self.add_component(self.lines_checkbox)

        way_label = Label("Czy chcesz żeby cząsteczki cieczy/gazu były widoczne:", pos_x=35, pos_y=125)
        self.add_component(way_label)

        self.drawable_checkbox = CheckBox(pos_x=480, pos_y=133, radius=10)
        self.drawable_checkbox.checked = True
        self.add_component(self.drawable_checkbox)

        temperature_label = Label("Temperatura cieczy/gazu [K]:", pos_x=60, pos_y=160)
        self.add_component(temperature_label)

        self.temperature_input = InputText(200, 30, 300, 155, default=293)
        self.add_component(self.temperature_input)



        start_text = Text("Start", (0, 0, 0), pos_x = 300, pos_y=105)
    
        self.start_but = Button(200, 30, 200, 550, start_text, self.start_simulation, (100, 100, 100), (80, 80, 80))
        self.add_component(self.start_but)

        pos_y_liquid = 200
        way_label = Label("CZĄSTECZKI CIECZY/GAZU:", pos_x=160, pos_y=pos_y_liquid)
        self.add_component(way_label)

        num_particles_label = Label("Liczba cząsteczek", pos_x=150, pos_y=pos_y_liquid+30)
        self.add_component(num_particles_label)

        self.particles_input = InputText(200, 30, 300, pos_y_liquid+25, default=500)
        self.add_component(self.particles_input)

        radius_particles_label = Label("Promień cząsteczek", pos_x=130, pos_y=pos_y_liquid+80)
        self.add_component(radius_particles_label)

        self.radius_particles_input = InputText(200, 30, 300, pos_y_liquid+75, default=1)
        self.add_component(self.radius_particles_input)

        mass_particles_label = Label("Masa atomowa cząsteczek [u]", pos_x=50, pos_y=pos_y_liquid+130)
        self.add_component(mass_particles_label)

        self.mass_particles_input = InputText(200, 30, 300, pos_y_liquid+125, default=5)
        self.add_component(self.mass_particles_input)


        pos_y_bounce = 375
        way_label = Label("CZĄSTECZKI ODBIJANE:", pos_x=210, pos_y=pos_y_bounce)
        self.add_component(way_label)

        num_particles_label = Label("Liczba cząsteczek", pos_x=150, pos_y=pos_y_bounce+30)
        self.add_component(num_particles_label)

        self.brownian_input = InputText(200, 30, 300, pos_y_bounce+25, default=1)
        self.add_component(self.brownian_input)

        radius_particles_label = Label("Promień cząsteczek", pos_x=130, pos_y=pos_y_bounce+80)
        self.add_component(radius_particles_label)

        self.radius_brownian_input = InputText(200, 30, 300, pos_y_bounce+75, default=5)
        self.add_component(self.radius_brownian_input)

        mass_particles_label = Label("Masa atomowa cząsteczek [u]", pos_x=50, pos_y=pos_y_bounce+130)
        self.add_component(mass_particles_label)

        self.mass_brownian_input = InputText(200, 30, 300, pos_y_bounce+125, default=10)
        self.add_component(self.mass_brownian_input)

    def start_simulation(self):
        """Method to prepare simulation on window
        """

        num_of_particles = int(self.particles_input.get_text())
        num_of_brownian = int(self.brownian_input.get_text())

        radius_particles = float(self.radius_particles_input.get_text())
        radius_brownian = float(self.radius_brownian_input.get_text())

        mass_particles = float(self.mass_particles_input.get_text())
        mass_brownian = float(self.mass_brownian_input.get_text())

        use_wiener = self.wiener_checkbox.checked
        drawable_particles = self.drawable_checkbox.checked
        show_lines = self.lines_checkbox.checked
        temperature = float(self.temperature_input.get_text())

        sim = Simulation(self.window, num_of_particles, radius_particles, mass_particles, drawable_particles,
                         num_of_brownian, radius_brownian, mass_brownian,  temperature, show_lines, use_wiener)

        sim.simulate()

    def add_component(self, component):
        """Method to add new component to window

        Args:
            component (GUIComponent): new component
        """

        self.gui_components.add(component)

    def update(self):
        """Update method
        """

        self.gui_components.update()   
        pygame.display.update()
        
    def fill(self):
        """Method to fill window with color
        """
        
        self.window.fill(self.fill_color)

    def draw(self):
        """Method to draw all components on window
        """
        
        for component in self.gui_components:
            component.draw(self.window)

    def start(self):
        """Main method
        """
        
        go = True

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go = False

                for component in self.gui_components:
                            component.handle_event(event)

            self.fill()
            self.draw()
            self.update()
