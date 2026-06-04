import pygame

from levels.map_loader import MapLoader
from settings import EXIT_COLOR, FLOOR_COLOR, ITEM_SIZE, KEY_COLOR, POTION_COLOR, TILE_SIZE, WALL_COLOR


class LevelManager:
    def __init__(self):
        self.loader = MapLoader()
        self.level_number = 1
        self.tiles = []
        self.spawn = (1, 1)
        self.exit = (1, 1)
        self.items = []

    def load_level(self, level_number):
        self.level_number = level_number
        data = self.loader.generate(level_number)
        self.tiles = data["tiles"]
        self.spawn = data["spawn"]
        self.exit = data["exit"]
        self.items = []
        for item in data["items"]:
            x, y = item["tile"]
            rect = pygame.Rect(0, 0, ITEM_SIZE, ITEM_SIZE)
            rect.center = (x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2)
            self.items.append({"id": item["id"], "tile": item["tile"], "rect": rect})

    def is_wall(self, x, y):
        if y < 0 or y >= len(self.tiles) or x < 0 or x >= len(self.tiles[0]):
            return True
        return self.tiles[y][x] == "#"

    def is_exit_reached(self, player):
        return player.tile_pos() == self.exit

    def draw(self, surface):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                color = WALL_COLOR if tile == "#" else FLOOR_COLOR
                pygame.draw.rect(surface, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(
            surface,
            EXIT_COLOR,
            (self.exit[0] * TILE_SIZE + 5, self.exit[1] * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10),
            border_radius=3,
        )
        for item in self.items:
            color = POTION_COLOR
            if item["id"] == "damage_boost" or item["id"] == "speed_boost":
                color = (151, 114, 255)
            elif item["id"] == "key":
                color = KEY_COLOR
            pygame.draw.rect(surface, color, item["rect"], border_radius=3)
