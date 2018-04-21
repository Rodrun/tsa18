"""The actual, complete powermeter.
"""
import pygame

from powermeter_bar import PowermeterBar as PmBar
from powermeter_tick import PowermeterTick as PmTick
from powermeter_percent import PowermeterPercent as PmPercent


class Powermeter(pygame.sprite.OrderedUpdates):

    def __init__(self, x, y, w, h, speed, show_percent=False,
                 percent_font=None, invisible=False):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed

        self.bar = PmBar(self.x, self.y, self.w, self.h, self.speed, invisible)
        self.tick = PmTick(self.bar, self.bar.rect.width // 2,
                           self.bar.rect.height // 10)

        self.add(self.bar)
        self.add(self.tick)
        if show_percent:
            self.percent = PmPercent(self.tick, percent_font)
            self.add(self.percent)
        else:
            self.percent = None

    def get_value(self, max=1):
        return self.tick.get_value() * max

    def set_speed(self, speed=0):
        self.speed = speed
        self.bar.speed = speed
