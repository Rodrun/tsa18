"""Display powermeter tick percentage.
"""
import math

import pygame
from pygame.transform import scale

from powermeter_tick import PowermeterTick


class PowermeterPercent(pygame.sprite.DirtySprite):

    def __init__(self, parent: PowermeterTick, font: pygame.font.Font = None,
                 color: tuple = (255, 0, 0), bg: tuple = None):
        """
            :param parent: parent PowermeterTick to attach to.
            :param font: font to use. None means default.
        """
        super().__init__()
        self.parent = parent
        if font is None:
            self.font = pygame.font.Font(None, parent.rect.width)
        else:
            self.font = font

        self.color = color
        self.bg = bg
        self.update()

    def update(self):
        pstr = self.percent_str(self.parent.get_value())
        self.image = self.font.render(pstr,
                                      0,
                                      self.color,
                                      self.bg)
        self.rect = scale(self.image,
                          (self.parent.rect.width,
                           self.parent.rect.height)).get_rect()
        self.update_pos()

    def update_pos(self):
        bottom = self.parent.rect.bottom
        left = self.parent.rect.left
        self.rect.top = bottom - self.rect.height
        self.rect.left = left

    def percent_str(self, per: float) -> str:
        return str(int(round(per * 100)))
