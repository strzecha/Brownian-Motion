import pygame
import random
from brownian.particle import Particle
from brownian.brownian import BrownianParticle

class Simulation:
    def __init__(self, num_of_particles=20):
        pygame.init()
        self.particles = pygame.sprite.Group()
        self.screen = pygame.display.set_mode([800, 600])

        for i in range(num_of_particles):
            self.particles.add(Particle(speedx=random.randint(-5, 5), speedy=random.randint(-5, 5)))

    def run(self):
        go = True
        timer = pygame.time.Clock()

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go = False
            
            self.screen.fill((0, 0, 0))
            self.particles.update()
            for particle in self.particles:
                particle.draw(self.screen)

                
            pygame.display.update()

            timer.tick(100)

    