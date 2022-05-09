import numpy as np
from brownian.particle import Particle

class BrownianParticle(Particle):
    def update_wiener(self):
        x_norm = np.random.normal()
        y_norm = np.random.normal()

        self.pos_x += x_norm
        self.pos_y += y_norm

        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        
