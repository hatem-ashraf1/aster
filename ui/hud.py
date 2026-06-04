import pygame

from settings import DARK_GRAY, HUD_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE


class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.small = pygame.font.Font(None, 22)

    def draw(self, surface, player, level_number, enemy_count, inventory):
        rect = pygame.Rect(0, SCREEN_HEIGHT - HUD_HEIGHT, SCREEN_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(surface, DARK_GRAY, rect)
        health_width = int(220 * max(0, player.health / player.max_health))
        pygame.draw.rect(surface, (78, 84, 96), (18, SCREEN_HEIGHT - 45, 220, 18), border_radius=4)
        pygame.draw.rect(surface, (86, 202, 121), (18, SCREEN_HEIGHT - 45, health_width, 18), border_radius=4)
        self._text(surface, f"HP {player.health}/{player.max_health}", 18, SCREEN_HEIGHT - 62)
        self._text(surface, f"Level {level_number}", 280, SCREEN_HEIGHT - 50)
        self._text(surface, f"Enemies {enemy_count}", 400, SCREEN_HEIGHT - 50)
        self._text(surface, f"Items {inventory.count()}", 540, SCREEN_HEIGHT - 50)
        self._text(surface, "Move WASD/Arrows  Shoot Space  Pause Esc  Save F5  Load F9", 18, SCREEN_HEIGHT - 22, small=True)

    def _text(self, surface, text, x, y, small=False):
        font = self.small if small else self.font
        surface.blit(font.render(text, True, WHITE), (x, y))
