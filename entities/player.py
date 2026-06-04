import pygame

from entities.projectile import Projectile
from settings import (
    PLAYER_COLOR,
    PLAYER_DAMAGE,
    PLAYER_FIRE_COOLDOWN,
    PLAYER_HEALTH,
    PLAYER_SPEED,
    TILE_SIZE,
)


class Player:
    def __init__(self, tile_pos):
        self.pos = pygame.Vector2(
            tile_pos[0] * TILE_SIZE + TILE_SIZE / 2,
            tile_pos[1] * TILE_SIZE + TILE_SIZE / 2,
        )
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.rect.center = self.pos
        self.max_health = PLAYER_HEALTH
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.damage = PLAYER_DAMAGE
        self.fire_cooldown = PLAYER_FIRE_COOLDOWN
        self.fire_timer = 0
        self.last_direction = pygame.Vector2(1, 0)

    def update(self, dt, keys, collision):
        self.fire_timer = max(0, self.fire_timer - dt)
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.last_direction = direction
            self._move_axis(direction.x * self.speed * dt, 0, collision)
            self._move_axis(0, direction.y * self.speed * dt, collision)

    def shoot(self):
        if self.fire_timer > 0:
            return None
        self.fire_timer = self.fire_cooldown
        return Projectile(self.rect.center, self.last_direction, self.damage)

    def apply_item(self, item_id):
        if item_id == "health_potion":
            self.health = min(self.max_health, self.health + 30)
        elif item_id == "damage_boost":
            self.damage += 5
        elif item_id == "speed_boost":
            self.speed += 12

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, border_radius=4)

    def tile_pos(self):
        return int(self.pos.x // TILE_SIZE), int(self.pos.y // TILE_SIZE)

    def _move_axis(self, dx, dy, collision):
        self.pos.x += dx
        self.pos.y += dy
        self.rect.center = self.pos
        if not collision.can_move_to(self.rect):
            self.pos.x -= dx
            self.pos.y -= dy
            self.rect.center = self.pos
