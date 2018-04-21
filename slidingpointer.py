"""Sliding pointer (made after powermeter).
"""
import pygame

import util


class SlidingPointer(pygame.sprite.DirtySprite):

    def __init__(self, parent_rect: pygame.rect.Rect, w, h,
                 speed=700, horizontal=True, up=True, left=False):
        """
            :param horizontal: horizontal?
            :param up: if horizontal, point up?
            :param left: if !horizontal, point to left?
        """
        super().__init__()
        self.parent_rect = parent_rect
        self.image = util.load_sized("resource/pointer.png", w, h)
        if not horizontal:
            rangle = -90 if not left else 90
            self.image = pygame.transform.rotate(self.image, rangle)
        elif horizontal and not up:
            self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()

        if horizontal:
            if up:
                # below parent
                self.rect.y = parent_rect.y + parent_rect.height
            else:
                # above parent
                self.rect.y = parent_rect.y - self.rect.height
            self.rect.x = self.extremes_respective(horizontal)[0]
        else:  # vertical
            if left:
                self.rect.x = self.parent_rect.x + self.rect.width
            else:  # point right, left of parent
                self.rect.x = self.parent_rect.x - self.rect.width
            self.rect.y = self.extremes_respective(horizontal)[0]

        self.speed = speed
        self.horizontal = horizontal
        self.left = left
        self.delta = 1

    def update(self):
        bounds = self.extremes_respective(self.horizontal)  #  parent bounds
        center = self.get_respective(self.horizontal)  # important value
        if center <= bounds[0] or center >= bounds[1]:
            self.set_respective(self.horizontal, (bounds[0] if center <= bounds[0] else bounds[1]) - self.length_respective(self.horizontal))
            self.speed = -self.speed

        self.accum_respective(self.horizontal, self.speed * self.delta)
        #print("speed \t= {}\nbounds \t={}\ncenter \t={}".format(self.speed, bounds, center))

    # *_respective deals with data respective to self.horizontal

    def get_respective(self, horizontal):
        center = self.rect.center
        return center[0] if horizontal else center[1]

    def extremes_respective(self, horizontal) -> tuple:
        """
        Get bound values, in (min, max) format.
        """
        if horizontal:  # left, right
            return (self.parent_rect.left, self.parent_rect.right)
        else:
            return (self.parent_rect.top, self.parent_rect.bottom)

    def accum_respective(self, horizontal, acc):
        rval = self.rect.x if horizontal else self.rect.y
        self.set_respective(self.horizontal, rval + acc)

    def length_respective(self, horizontal):
        if horizontal:
            return self.rect.width / 2
        else:
            return self.rect.height / 2

    def set_respective(self, horizontal, v):
        if horizontal:
            self.rect.x = v
        else:
            self.rect.y = v

    def get_value(self):
        return self.get_respective(self.horizontal)

    def set_delta(self, d):
        self.delta = d