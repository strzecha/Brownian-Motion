import pygame
import numpy as np

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos_x=400, pos_y=300, speedx=5, speedy=5, radius=5):
        super().__init__()

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speedx = speedx
        self.speedy = speedy

        self.image = pygame.Surface((2 * radius, 2 * radius))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        width, height = pygame.display.get_surface().get_size()

        if self.rect.bottom >= height or self.rect.top <= 0:
            self.speedy = -self.speedy
        if self.rect.left <= 0 or self.rect.right >= width:
            self.speedx = -self.speedx



        
