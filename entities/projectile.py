import pygame

from settings import PROJECTILE_COLOR, PROJECTILE_LIFETIME, PROJECTILE_RADIUS, PROJECTILE_SPEED


class Projectile:
    def __init__(self, pos, direction, damage):
        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2(direction)
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(1, 0)
        self.direction = self.direction.normalize()
        self.damage = damage
        self.lifetime = PROJECTILE_LIFETIME
        self.alive = True

    def update(self, dt):
        self.pos += self.direction * PROJECTILE_SPEED * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, PROJECTILE_COLOR, self.pos, PROJECTILE_RADIUS)
