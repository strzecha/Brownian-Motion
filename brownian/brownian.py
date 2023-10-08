import numpy.random as random
from brownian.particle import Particle

class BrownianParticle(Particle):
    def __init__(self, pos_x, pos_y, mass_atomic=1, radius=1, temperature=0, drawable=True, color=(255, 255, 255)):
        super().__init__(pos_x, pos_y, mass_atomic, radius, temperature, drawable, color)

    def update_wiener(self, screen):
        width, height = screen.get_size()
        
        x_norm = random.normal(scale=self.radius / 2)
        y_norm = random.normal(scale=self.radius / 2)

        self.pos_x += x_norm
        self.pos_y += y_norm

        self.rect.centerx = max(0, min(self.pos_x, width))
        self.rect.centery = max(0, min(self.pos_y, height))

        
