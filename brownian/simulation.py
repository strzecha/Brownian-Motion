import pygame
import numpy.random as random
import time

from brownian.particle import Particle
from brownian.brownian import BrownianParticle

class Simulation:
    def __init__(self, screen, num_of_particles=20, radius_particles=1, mass_particles=1, drawable_particles=True, num_of_brownian_particles=1, radius_brownian=5, mass_brownian=5, temperature=273, show_lines=True, use_wiener=False):
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
            self.update_simulation = self.update_wiener
            num_of_particles = 0
        else:
            self.update_simulation = self.update_physics

        self.prepare_particles(num_of_particles, radius_particles, mass_particles, drawable_particles, num_of_brownian_particles, radius_brownian, mass_brownian, temperature)

    def set_screen(self, screen):
        self.screen_width, self.screen_height = screen.get_size()
        self.screen = screen

    def prepare_particles(self, num_of_particles, radius_particles, mass_particles, drawable_particles, num_of_brownian_particles, radius_brownian, mass_brownian, temperature):

        for _ in range(num_of_particles):
            particle = Particle(pos_x=random.randint(0, self.screen_width), pos_y=random.randint(0, self.screen_height), 
                                mass_atomic=mass_particles, radius=radius_particles, temperature=temperature, drawable=drawable_particles)
            self.particles.add(particle)

        for _ in range(num_of_brownian_particles):
            brownian = BrownianParticle(pos_x=random.randint(self.screen_width // 2 - 50, self.screen_width // 2 + 50), 
                                pos_y=random.randint(self.screen_height // 2 - 50, self.screen_height // 2 + 50),
                                mass_atomic=mass_brownian, radius=radius_brownian, temperature=0,)
            self.particles.add(brownian)

    def get_contact_time(self, particle1, particle2):
        x1 = particle1.last_x
        y1 = particle1.last_y
        x2 = particle2.last_x
        y2 = particle2.last_y
        v1x = particle1.speedx
        v1y = particle1.speedy
        v2x = particle2.speedx
        v2y = particle2.speedy

        del_X = x2 - x1
        del_Y = y2 - y1
        del_Vx = v2x - v1x
        del_Vy = v2y - v1y

        del_VSq = del_Vx ** 2 + del_Vy ** 2
        r1 = particle1.radius
        r2 = particle2.radius
        SSq = (r1 + r2) ** 2
        del_s = del_X * del_Vx + del_Y * del_Vy
        del_r = del_X ** 2 + del_Y ** 2
        sq_root = del_s ** 2 - del_VSq * (del_r - SSq)

        if del_VSq < 0.000000001 or sq_root < 0:
            contact_time = self.last_time + 0.5 * (self.time - self.last_time)
        else:
            delT = (-del_s - sq_root ** 0.5) / del_VSq
            contact_time = self.last_time + delT
        return contact_time

    def collide_particles(self, particle1, particle2):
        v1x = particle1.speedx
        v2x = particle2.speedx
        v1y = particle1.speedy
        v2y = particle2.speedy

        contact_time = self.get_contact_time(particle1, particle2)

        delTBefore = contact_time - self.last_time
        delTAfter = self.time - contact_time

        x1 = particle1.last_x + v1x * delTBefore
        x2 = particle2.last_x + v2x * delTBefore
        y1 = particle1.last_y + v1y * delTBefore
        y2 = particle2.last_y + v2y * delTBefore
        delX = x2 - x1
        delY = y2 - y1
        d = max((delX ** 2 + delY ** 2) ** 0.5, 10 ** (-30))

        v1n = (1 / d) * (v1x * delX + v1y * delY)
        v2n = (1 / d) * (v2x * delX + v2y * delY)
        v1t = (1 / d) * (-v1x * delY + v1y * delX)
        v2t = (1 / d) * (-v2x * delY + v2y * delX)

        m1 = particle1.mass
        m2 = particle2.mass

        elasticity = 1
        v1nP = ((m1 - m2 * elasticity) * v1n + m2 * (1 + elasticity) * v2n) / (m1 + m2)
        v2nP = (elasticity + 0.000001) * (v1n - v2n) + v1nP

        particle1.speedx = (1 / d) * (v1nP * delX - v1t * delY)
        particle1.speedy = (1 / d) * (v1nP * delY + v1t * delX)
        particle2.speedx = (1 / d) * (v2nP * delX - v2t * delY)
        particle2.speedy = (1 / d) * (v2nP * delY + v2t * delX)

        particle1.rect.centerx = x1 + particle1.speedx * delTAfter
        particle1.rect.centery = y1 + particle1.speedy * delTAfter
        particle2.rect.centerx = x2 + particle2.speedx * delTAfter
        particle2.rect.centery = y2 + particle2.speedy * delTAfter

    def update_physics(self):
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
        for particle in self.particles:
            particle.update_wiener(self.screen)
            particle.draw(self.screen)

    def simulate(self):
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

                    if event.button == 3 and not self.use_wiener: # right click
                        particle = Particle(pos_x=pos_x, pos_y=pos_y, mass_atomic=self.mass_particles, radius=self.radius_particles,
                                             temperature=self.temperature, drawable=self.drawable_particles)
                        self.particles.add(particle)

                    elif event.button == 1: #left click
                        brownian = BrownianParticle(pos_x=pos_x, pos_y=pos_y, mass_atomic=self.mass_brownian, radius=self.radius_brownian,
                                                     temperature=0,)
                        self.particles.add(brownian)




            if not self.show_lines:
                self.screen.fill((0, 0, 0))

            self.update_simulation()
            pygame.display.update()

            timer.tick(100)
