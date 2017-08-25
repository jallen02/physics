import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

height = 600
width = 600
ball_radius = 20
ball_mass = 1
gravity = (0.0, 900)
starting_point = (50, 50)
line_width = 1

def add_ball(space, pos):
    mass = ball_mass
    radius = ball_radius
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass,moment)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return shape

def add_line(space, pos1, pos2):
    vector = (pos2[0]-pos1[0], pos2[1]-pos1[1])

    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos1
    line = pymunk.Segment(body, (0,0), vector, line_width)
    
    space.add(line)
    return line

def draw_balls(screen, balls):
    for ball in balls:
        p = int(ball.body.position.x), int(ball.body.position.y)
        pygame.draw.circle(screen, pygame.color.THECOLORS["blue"], p, ball_radius)

def draw_lines(screen, lines):
    for line in lines:
        p1 = line.body.position + line.a
        p2 = line.body.position + line.b
        pygame.draw.line(screen,pygame.color.THECOLORS["black"], p1, p2, 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((height, width))
    pygame.display.set_caption("Simple Ramp-Making")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = gravity

    balls = []
    lines = []
    draw_preview = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN:
                pos1 = pygame.mouse.get_pos()
                draw_preview = True
            elif event.type == MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                lines.append(add_line(space, pos1, pos2))
                draw_preview = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                balls.append(add_ball(space, starting_point))

        screen.fill((255,255,255))
        
        pygame.draw.circle(screen, pygame.color.THECOLORS["blue"], starting_point, ball_radius, 2)

        if draw_preview:
            pygame.draw.line(screen, pygame.color.THECOLORS["lightgray"], \
                             pos1, pygame.mouse.get_pos())

        draw_lines(screen, lines)
        draw_balls(screen, balls)
        for ball in balls:
            if ball.body.position.x > width + ball_radius or \
                    ball.body.position.y > height + ball_radius:
                space.remove(ball)
                balls.remove(ball)

        space.step(1/50.0)

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    sys.exit(main())
