"""
"""
import pygame

import util

class Touchzone(pygame.sprite.Sprite):

    def __init__(self, y, w, h):
        super().__init__()
        self.image = util.load_sized("resource/circle.png", w, h)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y
