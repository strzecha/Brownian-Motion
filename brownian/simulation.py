import pygame
from brownian.brownian import BrownianParticle

class Simulation:
    def __init__(self, num_of_particles=20):
        pygame.init()
        self.particles = list()
        self.screen = pygame.display.set_mode([800, 600])

        for i in range(num_of_particles):
            self.particles.append(BrownianParticle())

    def run(self):
        go = True

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go = False

            for particle in self.particles:
                particle.draw(self.screen)
            pygame.display.update()

    