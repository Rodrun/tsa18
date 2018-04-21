"""Tick mark for powermeter. (The arrow)
"""
import pygame
from pygame.transform import scale

from powermeter_bar import PowermeterBar
import util


class PowermeterTick(pygame.sprite.Sprite):

    def __init__(self, parent: PowermeterBar, w, h):
        """
            :param parent: parent power meter.
        """
        super().__init__()
        self.parent = parent
        self.w = w
        self.h = h
        self.speed = self.parent.speed
#        self.image = scale(pygame.image.load("resource/tick.png").convert(),
#                           (w, h))
        self.image = util.load_sized("resource/tick.png", w, h)
        self.rect = self.image.get_rect()
        self.rect.x = self.parent.rect.x - self.w
        self.rect.y = self.parent.rect.top + (self.rect.height / 2)

    def update(self):
        if self.parent.moving:
            midy = self.get_midY()  # Too lazy to change it in the if statement
            if midy <= self.parent.rect.y or \
                    midy >= self.parent.rect.bottom:
                self.speed = -self.speed
            self.rect.top += self.speed

    def get_midY(self):
        return self.rect.center[1]

    def get_value(self):
        """
        Get the percent value.
        """
        ry = self.parent.rect.bottom - self.get_midY()
        percent = ry / self.parent.rect.height
        return abs(percent)  # Since it's flipped

    def set_speed(self, s):
        if self.speed < 0:
            self.speed = -s
        elif self.speed >= 0:
            self.speed = s
