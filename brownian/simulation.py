import pygame
import numpy.random as random
import time

from brownian.particle import Particle
from brownian.brownian import BrownianParticle

class Simulation:
    """Class Simulation
    
    Class to show simulation of Brownian motion
    """

    def __init__(self, screen, num_of_particles=20, radius_particles=1, mass_particles=1, drawable_particles=True, num_of_brownian_particles=1, radius_brownian=5, mass_brownian=5, temperature=273, show_lines=True, use_wiener=False):
        """Init method

        Args:
            screen (Window): screen
            num_of_particles (int, optional): number of common particles in simulation. Defaults to 20.
            radius_particles (int, optional): radius of common particles. Defaults to 1.
            mass_particles (int, optional): atomic mass of common particles. Defaults to 1.
            drawable_particles (bool, optional): if common particles should be drawn on screen. Defaults to True.
            num_of_brownian_particles (int, optional): number of Brownian particles in simulation. Defaults to 1.
            radius_brownian (int, optional): radius of Brownian particles. Defaults to 5.
            mass_brownian (int, optional): atomis mass of Brownian particles. Defaults to 5.
            temperature (int, optional): temperature in simulation. Defaults to 273.
            show_lines (bool, optional): if route of all particles should be drawn on screen. Defaults to True.
            use_wiener (bool, optional): if this simulation should simulate Wiener cycle. Defaults to False.
        """

        pygame.init()

        self.particles = pygame.sprite.Group()
        
        self.screen_width = 0
        self.screen_height = 0

        self.last_time = 0
        self.time = 0

        self.show_lines = show_lines

        self.num_of_particles = num_of_particles
        self.radius_particles = radius_particles
        self.mass_particles = mass_particles
        self.num_of_brownian_particles = num_of_brownian_particles
        self.radius_brownian = radius_brownian
        self.mass_brownian = mass_brownian
        self.temperature = temperature
        self.drawable_particles = drawable_particles
        self.use_wiener = use_wiener
        self.set_screen(screen)
        
        if use_wiener:
            # Wiener cycle
            self.update_simulation = self.update_wiener
            self.num_of_particles = 0
        else:
            # Brownian motion
            self.update_simulation = self.update_physics

        self.prepare_particles()

    def set_screen(self, screen):
        """Screen setter

        Args:
            screen (Window): screen
        """
        self.screen_width, self.screen_height = screen.get_size()
        self.screen = screen

    def prepare_particles(self):
        """Method to create particles in simulation
        """

        for _ in range(self.num_of_particles):
            particle = Particle(pos_x=random.randint(0, self.screen_width), pos_y=random.randint(0, self.screen_height), 
                                mass_atomic=self.mass_particles, radius=self.radius_particles, temperature=self.temperature, drawable=self.drawable_particles)
            self.particles.add(particle)

        for _ in range(self.num_of_brownian_particles):
            brownian = BrownianParticle(pos_x=random.randint(self.screen_width // 2 - 50, self.screen_width // 2 + 50), 
                                pos_y=random.randint(self.screen_height // 2 - 50, self.screen_height // 2 + 50),
                                mass_atomic=self.mass_brownian, radius=self.radius_brownian, temperature=0,)
            self.particles.add(brownian)

    def get_contact_time(self, particle1, particle2):
        """Method to calculate contact time of two particles

        Args:
            particle1 (Particle): first particle
            particle2 (Particle): second particle

        Returns:
            float: contact time
        """

        delta_x = particle2.last_x - particle1.last_x
        delta_y = particle2.last_y - particle1.last_y
        delta_speed_x = particle2.speed_x - particle1.speed_x
        delta_speed_y = particle2.speed_y - particle1.speed_y

        delta_speed_square = delta_speed_x ** 2 + delta_speed_y ** 2
        delta_s = delta_x * delta_speed_x + delta_y * delta_speed_y
        sq_root = delta_s ** 2 - delta_speed_square * (delta_x ** 2 + delta_y ** 2 - (particle1.radius + particle2.radius) ** 2)

        if delta_speed_square < 1e-9 or sq_root < 0:
            contact_time = self.last_time + 0.5 * (self.time - self.last_time)
        else:
            delta_time = (-delta_s - sq_root ** 0.5) / delta_speed_square
            contact_time = self.last_time + delta_time

        return contact_time

    def collide_particles(self, particle1, particle2):
        """Method to perform collision of two particles

        Args:
            particle1 (Particle): first particle
            particle2 (Particle): second particle
        """

        contact_time = self.get_contact_time(particle1, particle2)

        delta_time_before = contact_time - self.last_time
        delta_time_after = self.time - contact_time

        x1 = particle1.last_x + particle1.speed_x * delta_time_before
        x2 = particle2.last_x + particle2.speed_x * delta_time_before
        y1 = particle1.last_y + particle1.speed_y * delta_time_before
        y2 = particle2.last_y + particle2.speed_y * delta_time_before
        delta_x = x2 - x1
        delta_y = y2 - y1
        d = max((delta_x ** 2 + delta_y ** 2) ** 0.5, 10 ** (-30))

        v1n = (1 / d) * (particle1.speed_x * delta_x + particle1.speed_y * delta_y)
        v2n = (1 / d) * (particle2.speed_x * delta_x + particle2.speed_y * delta_y)
        v1t = (1 / d) * (-particle1.speed_x * delta_y + particle1.speed_y * delta_x)
        v2t = (1 / d) * (-particle2.speed_x * delta_y + particle2.speed_y * delta_x)

        elasticity = 1
        v1nP = ((particle1.mass - particle2.mass * elasticity) * v1n + particle2.mass * (1 + elasticity) * v2n) / (particle1.mass + particle2.mass)
        v2nP = (elasticity + 0.000001) * (v1n - v2n) + v1nP

        particle1.speed_x = (1 / d) * (v1nP * delta_x - v1t * delta_y)
        particle1.speed_y = (1 / d) * (v1nP * delta_y + v1t * delta_x)
        particle2.speed_x = (1 / d) * (v2nP * delta_x - v2t * delta_y)
        particle2.speed_y = (1 / d) * (v2nP * delta_y + v2t * delta_x)

        particle1.rect.centerx = x1 + particle1.speed_x * delta_time_after
        particle1.rect.centery = y1 + particle1.speed_y * delta_time_after
        particle2.rect.centerx = x2 + particle2.speed_x * delta_time_after
        particle2.rect.centery = y2 + particle2.speed_y * delta_time_after

    def update_physics(self):
        """Method to update particles with physics rules
        """

        for particle in self.particles:
            self.particles.remove(particle)
            particle.update(time.time() - (self.start_time + self.time), self.screen)
            
            particle.draw(self.screen)
            hits = pygame.sprite.spritecollide(particle, self.particles, False)

            for hit in hits:
                self.collide_particles(particle, hit)

            self.particles.add(particle)

        self.last_time = self.time
        self.time += (time.time() - (self.start_time + self.time))

    def update_wiener(self):
        """Method to update particles with Wienen cycle
        """

        for particle in self.particles:
            particle.update_wiener(self.screen)
            particle.draw(self.screen)

    def simulate(self):
        """Method to run simulation
        """

        go = True
        self.time = 0
        self.start_time = time.time()
        timer = pygame.time.Clock()
        self.screen.fill((0, 0, 0))

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        go = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()

                    # right click - add common particle
                    if event.button == 3 and not self.use_wiener:
                        particle = Particle(pos_x=pos_x, pos_y=pos_y, mass_atomic=self.mass_particles, radius=self.radius_particles,
                                             temperature=self.temperature, drawable=self.drawable_particles)
                        self.particles.add(particle)

                    # left click - add Brownian particle
                    elif event.button == 1:
                        brownian = BrownianParticle(pos_x=pos_x, pos_y=pos_y, mass_atomic=self.mass_brownian, radius=self.radius_brownian,
                                                     temperature=0,)
                        self.particles.add(brownian)

            if not self.show_lines:
                self.screen.fill((0, 0, 0))

            self.update_simulation()
            pygame.display.update()

            timer.tick(100)
