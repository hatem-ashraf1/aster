import pygame


class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def image(self, path):
        if path not in self.images:
            self.images[path] = pygame.image.load(path).convert_alpha()
        return self.images[path]

    def sound(self, path):
        if path not in self.sounds:
            self.sounds[path] = pygame.mixer.Sound(path)
        return self.sounds[path]
