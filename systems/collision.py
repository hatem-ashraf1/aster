import pygame

from settings import TILE_SIZE


class CollisionSystem:
    def __init__(self, level_manager):
        self.level_manager = level_manager

    def can_move_to(self, rect):
        for tile in self.tiles_for_rect(rect):
            if self.level_manager.is_wall(*tile):
                return False
        return True

    def projectile_hit_wall(self, projectile):
        tile_x = int(projectile.pos.x // TILE_SIZE)
        tile_y = int(projectile.pos.y // TILE_SIZE)
        return self.level_manager.is_wall(tile_x, tile_y)

    def collect_items(self, player, inventory):
        collected = []
        for item in list(self.level_manager.items):
            if player.rect.colliderect(item["rect"]):
                inventory.add_item(item["id"])
                player.apply_item(item["id"])
                self.level_manager.items.remove(item)
                collected.append(item)
        return collected

    @staticmethod
    def projectile_hits_enemy(projectile, enemy):
        return enemy.rect.collidepoint(projectile.pos.x, projectile.pos.y)

    @staticmethod
    def tiles_for_rect(rect):
        left = rect.left // TILE_SIZE
        right = (rect.right - 1) // TILE_SIZE
        top = rect.top // TILE_SIZE
        bottom = (rect.bottom - 1) // TILE_SIZE
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                yield int(x), int(y)
