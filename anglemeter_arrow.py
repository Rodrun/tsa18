"""Angle meter arrow. Use this one.
"""
import pygame
from pygame.transform import scale

from util import rotate


class AnglemeterArrow(pygame.sprite.DirtySprite):

    def __init__(self, x, y, length, speed, width=20):
        super().__init__()
        self.image = pygame.image.load("resource/tick.png").convert()
        self.image = scale(self.image, (width, length))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = 1

    def update(self):
        self.image = rotate(self.image,
                            (self.rect.center[0], self.rect.center[1]),
                            self.angle)
        self.rect = self.image.get_rect()

    def set_speed(self, sp=0):
        self.speed = sp

    def get_angle(self):
        return self.angle
