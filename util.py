"""Utility
"""
import math

import pygame
from pygame.transform import scale
from pygame.image import load


def hypotenuse(a, b):
    return math.sqrt((a ** 2) + (b ** 2))


def distance(x1, x2, y1, y2):
    xdif = x2 - x1
    ydif = y2 - y1
    return math.sqrt((xdif ** 2) + (ydif ** 2))


def distance_r(r1: pygame.rect.Rect, r2: pygame.rect.Rect):
    # NOTE: from center
    return distance(r1.center[0], r2.center[0], r1.center[1], r2.center[1])


def contains(r1: pygame.rect.Rect, r2: pygame.rect.Rect):
    a = r1
    b = r2
    if a.right < b.right and a.x > b.x and a.y > b.y and a.bottom < b.bottom:
        return True
    else:
        return False


def find_angle(opp, adj):
    return math.atan(opp / adj)


def load_sized(path, w, h):
    return scale(load(path).convert_alpha(), (w, h))


def text_sized(s: str, font: pygame.font.Font, w, h, col, bg, antialias=1):
    return scale(font.render(s, antialias, col, bg), (w, h))

# do not use...
def rotate(img, pos, angle):
    w, h = img.get_size()
    img2 = pygame.Surface((w*2, h*2), pygame.SRCALPHA)
    #img2.blit(img, (w-pos[0], h-pos[1]))
    return pygame.transform.rotate(img2, angle)
