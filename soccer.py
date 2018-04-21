"""Soccer gamemode

Handles the logic of certain objects

bg not included
"""
from random import randrange
import math

import pygame
from pygame.image import load
from pygame.transform import scale

from blinkingmessage import BlinkingMessage
from soccerball import Soccerball
from slidingpointer import SlidingPointer
from dramatictext import DramaticText
from goal import Goal
import util


# Soccer states
NEW_TARGET      = 1  # Generate new target and reset everything except score
POLL_HORIZ      = 2  # Poll horizontal
POLL_VERT       = 3  # Poll vertical
SHOOT           = 4  # Shoot
SHOT_PROG       = 5  # Shot in progress (tests for goal)
MISS            = 6  # Miss
GOAL            = 7  # Goal

COACH_IMG_CT    = 3  # Number of coach images
MULTIPLYER      = 1.5# Multiplier for tick speed after every goal no used
BALL_SPEED      = 800# Ball speed not used
MIN_PAD         = 10 # Minimum padding for targets
MAX_SHOTS       = 3  # Maximum amount of shots that can be taken

class Soccer:

    def __init__(self, goal_rect: pygame.rect.Rect, w, h, font: pygame.font.Font):
        """
            :param goalrect: goal boundaries
            :param w: screen w
            :param h: screen h
        """
        self.goal_rect = goal_rect
        self.w = w
        self.h = h
        self.goals = 0
        self.shots = 0
        self.lost = False
        self.state = NEW_TARGET
        self.target_rect = None  # to be generated
        self.state_tick = 0
        self.space_action = False
        
        self.target_img = util.load_sized("resource/target.png", 1, 1)
        self.dest_x = 0
        self.dest_y = 0

        self.group = pygame.sprite.OrderedUpdates()
        self.goal = Goal(self.goal_rect.x, self.goal_rect.y, self.goal_rect.width, self.goal_rect.height)
        self.ball = Soccerball(w / 2, h - (h // 8 + 5), self.goal.rect.width // 8, self.goal.rect.width // 8)
        self.group.add(self.ball)

        self.coach_w = w // 9
        self.coach_h = h // 4
        self.coach_number = 0
        self.coach_imgs = {}
        for n in range(0, COACH_IMG_CT):
            name = "resource/coach" + str(n) + ".png"
            self.coach_imgs[str(n)] = util.load_sized(name, self.coach_w,
                                                      self.coach_h)
        self.coach_coord = (w - self.coach_w, h - self.coach_h)

        self.g_group = pygame.sprite.GroupSingle()
        self.xpointer = SlidingPointer(self.goal_rect, 100, 100)
        self.ypointer = SlidingPointer(self.goal_rect, 100, 100, horizontal=False, left=False)

        self.show_dust = False
        self.dust = util.load_sized("resource/dust.png", self.ball.rect.width, self.ball.rect.height)

        self.dramatic = DramaticText(w, h, font)
        self.press_space = BlinkingMessage(font, "PRESS SPACE! ", 100, 100,
                                      w // 8, h // 11)
        self.score_table = BlinkingMessage(font, "SCORE: 0 | MISS: 0", w / 2, 100, h // 5, h // 11)

    def update(self, delta=1):
        self.dramatic.update()
        self.g_group.update()
        self.group.update()
        self.press_space.update()
        self.score_table.update()

        self.ball.set_delta(delta)
        self.xpointer.set_delta(delta)
        self.ypointer.set_delta(delta)

        self.score_table.set_text("GOALS: {} | MISS: {}".format(self.goals, self.shots))
        if self.state == NEW_TARGET:
            self.state_tick = 0
            self.ball.reset()
            self.target_rect = self.generate_target(self.goal_rect)
            self.target_img = pygame.transform.scale(self.target_img, (self.target_rect.width, self.target_rect.height))
            self.state = POLL_HORIZ
        elif self.state == POLL_HORIZ:
            if self.xpointer not in self.g_group:
                self.g_group.add(self.xpointer)
            if self.space_action:
                self.dest_x = self.xpointer.get_value()
                self.state = POLL_VERT
        elif self.state == POLL_VERT:
            if self.ypointer not in self.g_group:
                self.g_group.add(self.ypointer)
            if self.space_action:
                self.dest_y = self.ypointer.get_value()
                self.state = SHOOT
        elif self.state == SHOOT:
            self.show_dust = True
            self.ball.center = (self.dest_x, self.dest_y)
            self.state = SHOT_PROG
        elif self.state == SHOT_PROG:
            if self.dest_x > self.target_rect.x and self.dest_x < self.target_rect.x + self.target_rect.width and\
                self.dest_y > self.target_rect.y and self.dest_y < self.target_rect.y + self.target_rect.height:
                self.state = GOAL
                self.coach_number -= 1
                self.goals += 1
                self.dramatic.show_text(1)
            else:
                self.state = MISS
                self.shots += 1
                self.coach_number += 1
                self.dramatic.show_text(0)
        elif self.state == MISS:
            self.show_dust = False
            if self.dramatic.done:
                self.state = NEW_TARGET
        elif self.state == GOAL:
            self.show_dust = False
            if self.dramatic.done:
                self.state = NEW_TARGET

        # Limit coach number
        if self.coach_number >= COACH_IMG_CT:
            self.coach_number = COACH_IMG_CT - 1
        elif self.coach_number < 0:
            self.coach_number = 0

        if self.shots >= MAX_SHOTS:
            self.lost = True

    def draw(self, sfc: pygame.Surface):
        self.group.draw(sfc)
        self.g_group.draw(sfc)
        self.goal.draw(sfc)
        if self.target_rect is not None:
            sfc.blit(self.target_img, (self.target_rect.x, self.target_rect.y))
        if self.show_dust:
            sfc.blit(self.dust, self.ball.init_rect)
        self.press_space.draw(sfc)
        self.score_table.draw(sfc)
        sfc.blit(self.coach_imgs[str(self.coach_number)], self.coach_coord)
        self.dramatic.draw(sfc)

    def generate_target(self, bounds: pygame.rect.Rect) -> pygame.rect.Rect:
        w = randrange(self.ball.rect.width + MIN_PAD, bounds.width - (2 * MIN_PAD))
        h = randrange(self.ball.rect.height + MIN_PAD, bounds.height - (2 * MIN_PAD))
        x = randrange(bounds.x, bounds.x + bounds.width - w)
        y = randrange(bounds.y, bounds.y + bounds.height - h)
        return pygame.rect.Rect((x, y), (w, h))

    def reset(self):
        self.goals = 0
        self.lost = False
        self.shots = 0
        self.state = NEW_TARGET

    def get_coach_img(self, n: int):
        return self.coach_imgs[str(n)]

    def get_points(self):
        return self.goals
