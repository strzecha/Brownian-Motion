import pygame
import numpy as np

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 255, 0)

R = 8.31446261815324 # J / (mol * K)
K_b = 1.380649 * 10 ** (-23)

# vsr = sqrt ( 3 * K_b * T / m )
# M - mol mass

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, mass_atomic=1, radius=1, temperature=0, drawable=False, color=(0, 0, 255)):
        super().__init__()

        self.image = pygame.Surface((2 * radius, 2 * radius))
        self.rect = self.image.get_rect()

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.last_x = self.rect.centerx
        self.last_y = self.rect.centery

        self.radius = radius
        self.mass = mass_atomic * 0.166 * 10 ** (-26) # kg
        self.temperature = temperature

        self.speed_avg = (3 * K_b * temperature / self.mass) ** 0.5
        self.speedx = np.random.uniform(-self.speed_avg, self.speed_avg)
        self.speedy = (self.speed_avg ** 2 - self.speedx ** 2) ** 0.5 * (1 if np.random.random() > 0.5 else -1)

        self.drawable = drawable
        self.color = color

    def draw(self, screen):
        if self.drawable:
            pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def update(self, time_in_seconds, screen):
        self.last_x = self.rect.centerx
        self.last_y = self.rect.centery 

        self.pos_x += self.speedx * time_in_seconds
        self.pos_y += self.speedy * time_in_seconds
        self.rect.centerx = self.pos_x + self.radius
        self.rect.centery = self.pos_y + self.radius

        width, height = screen.get_size()

        if self.rect.bottom >= height: 
            self.speedy = -self.speedy
            self.rect.bottom = height
        if self.rect.top <= 0:
            self.speedy = -self.speedy
            self.rect.top = 0
        if self.rect.left <= 0:
            self.speedx = -self.speedx
            self.rect.left = 0
        if self.rect.right >= width:
            self.speedx = -self.speedx
            self.rect.right = width
