import pygame
import numpy as np

class BrownianParticle:
    def __init__(self, pos_x=400, pos_y=300, radius=5):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.pos_x, self.pos_y), self.radius)

    def update(self):
        x_norm = np.random.normal()
        y_norm = np.random.normal()

        self.pos_x += x_norm
        self.pos_y += y_norm

        
