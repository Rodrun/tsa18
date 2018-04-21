"""Dramatic text (slides across screen FROM the right)
"""
import pygame

import util


class DramaticText:

    def __init__(self, w, h, font: pygame.font.Font, speed=25, pause_duration=15,
                 fg=(255, 255, 255), bg=(0, 0, 0)):
        self.w = w # given w (should be display w)
        self.h = h # given h ^
        self.x = w
        self.y = h / 2 - (h // 7)
        self.speed = speed

        self.miss = util.text_sized("MISS!", font, w // 6, h // 7, fg, bg)
        self.bg = bg
        self.goal = util.text_sized("POINT!", font, w // 6, h // 7, fg, bg)

        self.done = True
        self.state = 0
        self.image = self.goal
        self.bar_rect = pygame.rect.Rect((0, self.y), (w, h // 7))

        self.has_paused = False  # Trigger
        self.pausing = False  # Pause state
        self.pause_duration = pause_duration
        self.pause_count = 0  # count ticks when 'paused'

    def update(self):
        if not self.done:
            # check to pause
            if self.x <= self.w // 2 and not self.has_paused:
                self.pausing = True
                self.pause_count = 0
            if self.pausing:
                self.has_paused = True
                self.pause_count += 1
                if self.pause_count >= self.pause_duration:
                    self.pausing = False
            else:
                self.x -= self.speed

            if self.x + self.image.get_rect().width <= 0:
                self.x = self.w
                self.current_speed = self.speed
                self.pause_count = 0
                self.pausing = False
                self.has_paused = False
                self.done = True

    def draw(self, surface: pygame.Surface):
        """
            :param mes: 0 = none, 1 = win, 2 = goal
        """
        if not self.done:
            # bar
            pygame.draw.rect(surface, self.bg, self.bar_rect)
            # message
            surface.blit(self.image, (self.x, self.y))

    def show_text(self, m: int, cb = None) -> bool:
        """
        0 for miss, anything else for goal
        """
        if m == 0:
            self.image = self.miss
        else:
            self.image = self.goal
        self.done = False