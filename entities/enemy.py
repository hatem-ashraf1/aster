import pygame

from settings import ENEMY_ATTACK_COOLDOWN, ENEMY_ATTACK_RANGE, ENEMY_COLOR, TILE_SIZE


class Enemy:
    def __init__(self, tile_pos, health, speed, damage):
        self.pos = pygame.Vector2(
            tile_pos[0] * TILE_SIZE + TILE_SIZE / 2,
            tile_pos[1] * TILE_SIZE + TILE_SIZE / 2,
        )
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.rect.center = self.pos
        self.health = health
        self.speed = speed
        self.damage = damage
        self.attack_range = ENEMY_ATTACK_RANGE
        self.attack_cooldown = ENEMY_ATTACK_COOLDOWN
        self.attack_timer = 0
        self.path_refresh = 0
        self.path = []

    def update(self, dt, player, pathfinder, collision):
        self.path_refresh -= dt
        if self.path_refresh <= 0:
            self.path = pathfinder.find_path(self.tile_pos(), player.tile_pos())
            self.path_refresh = 0.35

        if self.path:
            target_tile = self.path[0]
            target = pygame.Vector2(
                target_tile[0] * TILE_SIZE + TILE_SIZE / 2,
                target_tile[1] * TILE_SIZE + TILE_SIZE / 2,
            )
            direction = target - self.pos
            if direction.length() < 3:
                self.path.pop(0)
            elif direction.length_squared() > 0:
                direction = direction.normalize()
                self._move_axis(direction.x * self.speed * dt, 0, collision)
                self._move_axis(0, direction.y * self.speed * dt, collision)

    def can_attack(self, player):
        return self.pos.distance_to(player.pos) <= self.attack_range

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect, border_radius=4)

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
