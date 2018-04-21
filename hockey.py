"""hockey faceoff game
likely one of the ugliest, most rushed things i've written to date.
"""
from random import randrange

import pygame

from puck import Puck
from touchzone import Touchzone
from dramatictext import DramaticText
from blinkingmessage import BlinkingMessage
import util

MAX_MISS = 3

START = 0
DROP = 1
DETERMINE = 2
LOSE = 2.5
RESET = 3

class Hockey:
    
    def __init__(self, w, h, font, pts):
        self.maxpts = pts
        self.w = w
        self.h = h
        self.pw = w // 8
        self.ph = h // 10
        self.ground = h - ((h / 3) * 2)
        self.touchzone = Touchzone(self.ground, w, h // 6)
        self.puck = Puck(w // 2 - (.5 * self.pw), 0, self.pw, self.ph, self.touchzone.rect.bottom, 900, 1500)
        self.stick = util.load_sized("resource/stick.png", w // 4, h // 6)
        self.gr = pygame.sprite.OrderedUpdates()
        self.gr.add(self.touchzone)
        self.gr.add(self.puck)
        self.LO_LIM = h // 3
        self.HI_LIM = h - (h / 3)

        self.score = 0
        self.miss = 0
        self.lost = False
        self.state = START
        self.space_action = False
        self.dramatic = DramaticText(w, h, font)
        self.press_space = BlinkingMessage(font, "PRESS SPACE! ", 100, 255,
                                      w // 8, h // 11)

    def update(self, delta=1):
        self.delta = delta
        self.puck.delta = delta
        self.gr.update()
        self.press_space.update()
        self.dramatic.update()
        
        if self.state == START:
            self.reset(False)
            self.state = DROP
        elif self.state == DROP:
            if pygame.sprite.collide_rect(self.puck, self.touchzone) and not self.puck.touch_floor() and self.space_action:
                self.dramatic.show_text(1)
                self.score += 1
                self.press_space.set_text("SCORE: {}/{} ".format(self.score, self.maxpts))
                self.state = RESET
            elif self.space_action or self.puck.touch_floor(): # not collide at all
                self.dramatic.show_text(0)
                self.miss += 1
                self.state = RESET
        elif self.state == RESET:
            if self.dramatic.done:
                self.state = START

        if self.miss >= MAX_MISS:
            self.lost = True

    def draw(self, sf):
        self.gr.draw(sf)
        sf.blit(self.stick, (self.w // 4, self.h - (self.stick.get_rect().height)))
        self.press_space.draw(sf)
        self.dramatic.draw(sf)
        #pygame.draw.line(self.)

    def random_ground(self):
        self.set_ground(randrange(self.LO_LIM, self.HI_LIM))

    def set_ground(self, y):
        self.ground = y
        self.touchzone.rect.y = y
        self.puck.ground = self.touchzone.rect.bottom

    def reset(self, score_reset=True):
        self.state = START
        self.score = self.score if not score_reset else 0
        self.miss = self.miss if not score_reset else 0
        self.lost = False
        self.puck.reset()
        self.press_space.set_text("SCORE: {}/{} ".format(self.score, self.maxpts))
        self.random_ground()

    def get_points(self):
        return self.score