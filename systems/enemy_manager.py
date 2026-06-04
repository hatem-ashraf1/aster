import random

from entities.enemy import Enemy
from settings import (
    ENEMY_BASE_COUNT,
    ENEMY_COUNT_PER_LEVEL,
    ENEMY_DAMAGE,
    ENEMY_HEALTH,
    ENEMY_HEALTH_PER_LEVEL,
    ENEMY_SPEED,
    ENEMY_SPEED_PER_LEVEL,
)


class EnemyManager:
    def __init__(self):
        self.enemies = []

    def spawn_enemies(self, level_manager, player):
        rng = random.Random(level_manager.level_number * 137)
        count = ENEMY_BASE_COUNT + (level_manager.level_number - 1) * ENEMY_COUNT_PER_LEVEL
        health = ENEMY_HEALTH + (level_manager.level_number - 1) * ENEMY_HEALTH_PER_LEVEL
        speed = ENEMY_SPEED + (level_manager.level_number - 1) * ENEMY_SPEED_PER_LEVEL
        open_tiles = [
            (x, y)
            for y, row in enumerate(level_manager.tiles)
            for x, tile in enumerate(row)
            if tile == "." and abs(x - player.tile_pos()[0]) + abs(y - player.tile_pos()[1]) > 8
        ]
        rng.shuffle(open_tiles)
        self.enemies = [Enemy(tile, health, speed, ENEMY_DAMAGE) for tile in open_tiles[:count]]

    def update(self, dt, player, pathfinder, collision, combat):
        for enemy in self.enemies:
            enemy.update(dt, player, pathfinder, collision)
            combat.enemy_attack(enemy, player, dt)
        self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

    def draw(self, surface):
        for enemy in self.enemies:
            enemy.draw(surface)

    def get_active_enemies(self):
        return self.enemies

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
