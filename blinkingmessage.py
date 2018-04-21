"""Blinking message
"""
import pygame

import util

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class BlinkingMessage:

    def __init__(self, font: pygame.font.Font, msg: str, x, y, w, h,
                 ticks=30, col=WHITE, bg=BLACK):
        self.font = font
        self.fg = col
        self.bg = bg
        self.message = msg
        self.pos = (x, y)
        self.dim = (w, h)
        self.ticks = abs(ticks)
        self.tick_count = 0
        self.image = util.text_sized(msg, font, w, h, col, bg)
        self.visible = True

    def update(self):
        if self.tick_count < self.ticks:
            self.tick_count += 1
        else:
            self.tick_count = 0
            self.visible = not self.visible

    def draw(self, surface: pygame.Surface):
        if self.visible:
            surface.blit(self.image, self.pos)

    def set_text(self, s: str, dim: tuple = None):
        if dim is None:
            dim = self.dim
        if s != self.message: # diff message
            self.image = util.text_sized(s, self.font, dim[0], dim[1], self.fg, self.bg)
