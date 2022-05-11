import pygame
import math

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 255, 0)

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speedx=5, speedy=5, radius=1, density=1, drawable=False, color=(0, 0, 255)):
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
        self.mass = (4 / 3 * math.pi * radius ** 3) * density
        self.speedx = speedx * 50
        self.speedy = speedy * 50

        self.drawable = drawable
        self.color = color

    def draw(self, screen):
        if self.drawable:
            pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def update(self, time_in_seconds):
        self.last_x = self.rect.centerx
        self.last_y = self.rect.centery 

        self.pos_x += self.speedx * time_in_seconds
        self.pos_y += self.speedy * time_in_seconds
        self.rect.centerx = self.pos_x + self.radius
        self.rect.centery = self.pos_y + self.radius

        width, height = pygame.display.get_surface().get_size()

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
