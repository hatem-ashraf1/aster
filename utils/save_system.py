import json
from pathlib import Path

import pygame

from settings import SAVE_FILE


class SaveSystem:
    def __init__(self, path=SAVE_FILE):
        self.path = Path(path)

    def save(self, game):
        data = {
            "level": game.level_manager.level_number,
            "player_health": game.player.health,
            "player_position": [game.player.pos.x, game.player.pos.y],
            "inventory": game.inventory.to_dict(),
        }
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self):
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))

    @staticmethod
    def restore_player(player, data):
        player.health = min(player.max_health, int(data.get("player_health", player.max_health)))
        if "player_position" in data:
            player.pos = pygame.Vector2(data["player_position"])
            player.rect.center = player.pos
