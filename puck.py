"""puck
"""
import random

import pygame

import util


class Puck(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, ground, minspeed, maxspeed):
        super().__init__()
        self.image = util.load_sized("resource/puck.png", w, h)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.falling = True
        self.minspeed = minspeed
        self.maxspeed = maxspeed
        self.speed = self.minspeed
        self.delta = 1
        self.ground = ground


    def touch_floor(self):
        if self.rect.y >= self.ground:
            return True
        else:
            return False

    def update(self):
        if self.falling:
            self.rect.y += self.speed * self.delta
            if self.touch_floor():
                self.falling = False

    def reset(self):
        self.rect.y = 0
        self.falling = True
        self.speed = random.randrange(self.minspeed, self.maxspeed)
