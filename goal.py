"""Soccer goal
"""
import pygame

import util


class Goal:

    def __init__(self, x, y, w, h, thickness_percent=.01):
        self.rect = pygame.rect.Rect((x, y), (w, h))
        self.thickness = int(thickness_percent * self.rect.w)
        self.bar_top = util.load_sized("resource/bar_top.png", w + 2 * self.thickness, self.thickness)
        self.bar_side = util.load_sized("resource/bar_side.png", self.thickness, h)
        self.net = util.load_sized("resource/net.png", w, h)

    def update(self):
        pass
        
    def draw(self, surface: pygame.Surface):
        x = self.rect.x
        y = self.rect.y
        surface.blit(self.net, (x, y))
        # top
        surface.blit(self.bar_top, (x - self.thickness, y - self.thickness))
        # left
        surface.blit(self.bar_side, (x - self.thickness, y))
        # right
        surface.blit(self.bar_side, (x + self.rect.w, y))
