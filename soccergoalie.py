"""Soccer goalkeeper.
"""
import pygame
from soccerball import Soccerball


class SoccerGoalie(pygame.sprite.DirtySprite):

    def __init__(self, x, y, w, h, goal, ball: Soccerball):
        self.image = pygame.image.load("resource/soccer_goalie.png").convert()
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shot_taken = False

    def update(self):
        if self.shot_taken:  # Ball is heading towards goalie
            pass
        else:  # Set the middle position
            pass

    def shot_at(self, flag: bool):
        self.shot_taken = flag
