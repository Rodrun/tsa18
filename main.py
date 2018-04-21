"""
TSA 2018 programming project.

Author: Juan M.

Included:
0 Soccer minigame
1 Hockey minigame

Run: python main.py <Included>

Notes:
Does not reflect my usual programming practices; rushed production.
Contains VERY poor documentation...
"""
import sys
import argparse

import pygame

from soccer import Soccer
import util


WIN_POINTS = 5
FPS = 60.0

parser = argparse.ArgumentParser()
parser.add_argument("included",
                    type=int,
                    help="0 for soccer; 1 for hockey")
args = parser.parse_args()

pygame.init()
pygame.display.set_caption("Minigame")

disp_info = pygame.display.Info()
screen = pygame.display.set_mode((disp_info.current_w, disp_info.current_h),
                                 pygame.FULLSCREEN)
width, height = disp_info.current_w, disp_info.current_h

gamemode = args.included  # 1 for hockey
originalgm = args.included

# load resources
serif_font = pygame.font.Font("resource/chava/Chava-Regular.ttf", 128)
if gamemode == 0: # soccer
    background = util.load_sized("resource/soccer_background.png", width, height)
    goal_rect = pygame.rect.Rect((width / 6, height / 5), (width - (width // 3), height // 3))
    soccer = Soccer(goal_rect, width, height, serif_font)
elif gamemode == 1: # hockey
    hockey = None

# win loss images
retry_img = util.load_sized("resource/retry.png", width, height)
win_img = util.load_sized("resource/win.png", width, height)

space_action = False  # Main action key

clock = pygame.time.Clock()
ptime = clock.tick(FPS)
dt = 1
while True:
    space_action = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.key == pygame.K_SPACE:
                space_action = True
                print("space_action triggered")
    
    if gamemode == 0:
        soccer.space_action = space_action
        soccer.update(dt)
        if soccer.get_points() == WIN_POINTS:
            gamemode = 3
        elif soccer.lost:
            gamemode = 2
    elif gamemode == 1:
        hockey.space_action = space_action
        hockey.update(dt)
    if gamemode == 2:
        if space_action:
            if originalgm == 0:
                soccer.reset()
            else:
                hockey.reset()
            gamemode = originalgm


    screen.fill((255, 255, 255))
    if gamemode == 0:  # Soccer
        screen.blit(background, background.get_rect())
        soccer.draw(screen)
    elif gamemode == 1:  # Hockey
        pass
        #screen.blit(background, background.get_rect())
    elif gamemode == 2:  # retry
        screen.blit(retry_img, retry_img.get_rect())
    elif gamemode == 3:  # win
        screen.blit(win_img, win_img.get_rect())
        if space_action:
            sys.exit(0)

    pygame.display.flip()
    dt = clock.tick(FPS) / 1000.0
