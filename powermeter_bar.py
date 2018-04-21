"""Vertical power meter bar.
"""
import pygame


class PowermeterBar(pygame.sprite.DirtySprite):

    def __init__(self, x, y, w, h, speed=0, invisible=False):
        """
            :param w: width.
            :param h: height.
        """
        super().__init__()
        self.speed = speed
        self.moving = True
        if not invisible:
            self.image = util.load_sized("resource/meter.png", w, h)
        else:
            self.image = pygame.Surface((w, h))
            self.image.set_alpha(0)
            self.image.fill((0, 0, 0))
            self.visible = 0
        self.rect = self.image.get_rect()
        self.polling = True

        # position
        self.rect.left = x
        self.rect.top = y
