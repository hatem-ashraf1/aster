import pygame

from settings import BLACK, GRAY, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE


class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.selected = 0
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 38)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.options)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.options)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self.options[self.selected][1]
        return None

    def draw(self, surface):
        surface.fill(BLACK)
        title = self.title_font.render(self.title, True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, 150)))
        for index, (label, _) in enumerate(self.options):
            color = WHITE if index == self.selected else GRAY
            text = self.font.render(label, True, color)
            surface.blit(text, text.get_rect(center=(SCREEN_WIDTH / 2, 270 + index * 48)))
