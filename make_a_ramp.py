import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

height, width = 600

def add_line(space, pos1, pos2):
    vector = pos2 - pos1

    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos1
    line = pymunk.Segment(body, (

def draw_lines(screen, lines):
    for line in lines:
        pygame.draw.line(screen,pygame.color.THECOLORS["black"], 

def main():
    pygame.init()
    screen = pygame.display.set_mode((height, width))
    pygame.display.set_caption("Simple Ramp-Making")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    draw_preview = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                draw_preview = True;
            elif event.type == MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                draw_preview = False;

        screen.fill((255,255,255))
        
        pygame.draw.circle(screen, pygame.color.THECOLORS["blue"], (50,50), 20, 2)

        if draw_preview:
            pygame.draw.line(screen, pygame.color.THECOLORS["lightgray"], \
                             pos, pygame.mouse.get_pos())

        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
