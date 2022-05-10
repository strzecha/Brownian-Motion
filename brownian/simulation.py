import pygame
import random
import time
from brownian.particle import Particle
from brownian.brownian import BrownianParticle

class Simulation:
    def __init__(self, num_of_particles=20):
        pygame.init()
        self.particles = pygame.sprite.Group()
        self.screen = pygame.display.set_mode([800, 600])
        self.last_time = self.time = 0

        for i in range(num_of_particles):
            self.particles.add(Particle(pos_x=random.randint(0, 800), pos_y=random.randint(0, 600), speedx=random.randint(-5, 5), speedy=random.randint(-5, 5), radius=1))

        for i in range(5):
            brownian = Particle(pos_x=100 * i + 20, pos_y=100 * i + 20, speedx=0, speedy=0, radius=5, density=0.25)
            brownian.color = (255, 255, 255)
            brownian.drawable = True
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

        delX = x2 - x1
        delY = y2 - y1
        delVx = v2x - v1x
        delVy = v2y - v1y

        delVSq = delVx * delVx + delVy * delVy
        r1 = particle1.radius
        r2 = particle2.radius
        SSq = (r1 + r2) ** 2
        delRDotDelV = delX * delVx + delY * delVy
        delRSq = delX * delX + delY * delY
        underSqRoot = delRDotDelV * delRDotDelV - delVSq * (delRSq - SSq)

        if delVSq < 0.000000001 or underSqRoot < 0:
            contact_time = self.last_time + 0.5 * (self.time - self.last_time)
        else:
            delT = (-delRDotDelV - underSqRoot ** 0.5) / delVSq
            contact_time = self.last_time + delT
        return contact_time

    def collide_particles(self, particle1, particle2):
        contact_time = self.get_contact_time(particle1, particle2)

        delTBefore = contact_time - self.last_time
        delTAfter = self.time - contact_time

        v1x = particle1.speedx
        v2x = particle2.speedx
        v1y = particle1.speedy
        v2y = particle2.speedy

        x1 = particle1.last_x + v1x * delTBefore
        x2 = particle2.last_x + v2x * delTBefore
        y1 = particle1.last_y + v1y * delTBefore
        y2 = particle2.last_y + v2y * delTBefore
        delX = x2 - x1
        delY = y2 - y1
        d = (delX ** 2 + delY ** 2) ** 0.5

        v1n = (1 / d) * (v1x * delX + v1y * delY)
        v2n = (1 / d) * (v2x * delX + v2y * delY)
        v1t = (1 / d) * (-v1x * delY + v1y * delX)
        v2t = (1 / d) * (-v2x * delY + v2y * delX)

        m1 = particle1.mass
        m2 = particle2.mass

        elasticity = 1
        v1nP = ((m1 - m2 * elasticity) * v1n + m2 * (1 + elasticity) * v2n) / (m1 + m2)
        v2nP = (elasticity + 0.000001) * (v1n - v2n) + v1nP
        v1xP = (1 / d) * (v1nP * delX - v1t * delY)
        v1yP = (1 / d) * (v1nP * delY + v1t * delX)
        v2xP = (1 / d) * (v2nP * delX - v2t * delY)
        v2yP = (1 / d) * (v2nP * delY + v2t * delX)

        particle1.speedx = v1xP
        particle1.speedy = v1yP
        particle2.speedx = v2xP
        particle2.speedy = v2yP

        newXi = x1 + v1xP * delTAfter
        newYi = y1 + v1yP * delTAfter
        newXj = x2 + v2xP * delTAfter
        newYj = y2 + v2yP * delTAfter

        particle1.rect.centerx = newXi
        particle1.rect.centery = newYi
        particle2.rect.centerx = newXj
        particle2.rect.centery = newYj

    def run(self):
        go = True
        timer = pygame.time.Clock()
        self.time = 0
        start = time.time()

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go = False
            
            self.screen.fill((0, 0, 0))
            
            for particle in self.particles:
                self.particles.remove(particle)
                particle.update(time.time() - (self.time + start))
                particle.draw(self.screen)
                hits = pygame.sprite.spritecollide(particle, self.particles, False)

                for hit in hits:
                    self.collide_particles(particle, hit)

                self.particles.add(particle)

            pygame.display.update()
            self.last_time = self.time
            self.time += (time.time() - (self.time + start))

            timer.tick(100)

    