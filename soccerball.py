"""Soccer ball base class.
"""
import copy
import math

import pygame

import util

class Soccerball(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):
        super().__init__()
        self.speed = 0
        self.image = util.load_sized("resource/ball.png", w, h)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.init_rect = copy.copy(self.rect)
        self.kicked = False
        self.dest_pt = (self.rect.x, self.rect.y)
        self.angle = math.radians(90)
        self.delta = 1

    def set_delta(self, delta=1):
        self.delta = delta

    def kick(self, power, destX, destY): # setup
        self.angle = util.find_angle(destY - self.rect.center[1],
                                     destX - self.rect.center[0])
        self.speed = power

    def reset(self):
        self.kicked = False
        self.speed = 0
        self.rect = copy.copy(self.init_rect)

    def travel(self, angle):
        self.rect.x -= self.speed * math.sin(angle)
        self.rect.y -= self.speed * math.cos(angle)

    def get_center(self):
        return self.rect.center

    def distance_traveled(self):
        """
        from init rect pt
        """
        return util.distance_r(self.rect, self.init_rect)
