import numpy.random as random
from brownian.particle import Particle

class BrownianParticle(Particle):
    def __init__(self, pos_x, pos_y, radius=5, density=0.25, drawable=True, color=(255, 255, 255)):
        super().__init__(pos_x, pos_y, 0, 0, radius, density, drawable, color)

    def update_wiener(self):
        x_norm = random.normal()
        y_norm = random.normal()

        self.pos_x += x_norm
        self.pos_y += y_norm

        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        
