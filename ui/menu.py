import pygame

from settings import BLACK, GRAY, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE


class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.selected = 0
        self.option_rects = []
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 38)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.options[self.selected][1]
        elif event.type == pygame.MOUSEMOTION:
            hovered = self._option_at(event.pos)
            if hovered is not None:
                self.selected = hovered
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = self._option_at(event.pos)
            if clicked is not None:
                self.selected = clicked
                return self.options[clicked][1]
        return None

    def draw(self, surface):
        surface.fill(BLACK)
        title = self.title_font.render(self.title, True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, 150)))
        self.option_rects = []
        for index, (label, _) in enumerate(self.options):
            color = WHITE if index == self.selected else GRAY
            text = self.font.render(label, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, 270 + index * 48))
            click_rect = rect.inflate(80, 18)
            self.option_rects.append(click_rect)
            if index == self.selected:
                pygame.draw.rect(surface, (30, 36, 46), click_rect, border_radius=6)
            surface.blit(text, rect)

    def _option_at(self, position):
        for index, rect in enumerate(self.option_rects):
            if rect.collidepoint(position):
                return index
        return None
