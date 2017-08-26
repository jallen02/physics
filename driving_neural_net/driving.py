import sys, random, math
import pygame
from pygame.locals import *

height = 1000
width = 800
friction = .2

class Track:
    def __init__(self, track_info:str, color:(int,int,int), width:int):
        self.walls = [[]]
        self.set_walls(track_info)
        self.color = color
        self.width = width

    def set_walls(self, track_info:str):
        points = open(track_info).readlines()
        for point in points:
            if point.isspace():
                self.walls.append([])
            elif point.startswith("start_point"):
                self.start_point = (int(point.split()[1]), \
                                    int(point.split()[2]))
            elif point.startswith("start_angle"):
                self.start_angle = int(point.split()[1])
            else:
                point = point.split()
                self.walls[-1].append((int(point[0]), int(point[1])))
        print(self.walls)
            
    def draw(self, screen):
        for wall in self.walls:
            if len(wall) > 1:
                pygame.draw.lines(screen, self.color, False, wall, self.width)
 

class Car:
    def __init__(self, size:(int,int), color:(int, int, int), \
                 acc_rate:float, brake_rate:float, turn_rate:float, \
                 max_speed:float, track:Track):

        self.rect = pygame.Rect(track.start_point, size)
        self.angle = track.start_angle
        self.speed = 0
        self.acc_rate = acc_rate
        self.turn_rate = turn_rate
        self.brake_rate = brake_rate
        self.max_speed = max_speed
        self.x = float(track.start_point[0])
        self.y = float(track.start_point[1])

    def move(self):
        x_incr = math.cos(math.radians(self.angle))
        y_incr = math.sin(math.radians(self.angle))
        self.x += x_incr * self.speed
        self.y += y_incr * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.speed -= friction
        if self.speed < 0:
            self.speed = 0

    def turn(self, direction:float):
        self.angle += self.turn_rate*direction

    def accelerate(self):
        self.speed += self.acc_rate
        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def brake(self):
        self.speed -= self.brake_rate
        if (self.speed < 0):
            self.speed = 0

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.color.THECOLORS["blue"], \
                         self.rect)
 
           

def main():
    pygame.init()
    font = pygame.font.SysFont("monospace", 15)
    screen = pygame.display.set_mode((height, width))
    pygame.display.set_caption("Driiiiive!")
    clock = pygame.time.Clock()

    track = Track("track.txt", pygame.color.THECOLORS["black"], 2)

    cars = []
    #cars.append(Car((10, 10), (100, 100), 0, 1, 1, 1))

    user_car = Car((10, 10), pygame.color.THECOLORS["blue"], .5, 1, 10, 10, track)
    user_acc = False
    user_brake = False
    user_turn_right = False
    user_turn_left = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                elif event.key == K_UP:
                    user_acc = True
                elif event.key == K_DOWN:
                    user_brake = True
                elif event.key == K_LEFT:
                    user_turn_left = True
                elif event.key == K_RIGHT:
                    user_turn_right = True
            elif event.type == KEYUP:
                if event.key == K_UP:
                    user_acc = False
                elif event.key == K_DOWN:
                    user_brake = False
                elif event.key == K_LEFT:
                    user_turn_left = False
                elif event.key == K_RIGHT:
                    user_turn_right = False
        
        screen.fill((255, 255, 255))

        for car in cars:
            car.draw(screen)
            car.move()
        
        if user_acc:
            user_car.accelerate()
        if user_brake:
            user_car.brake()
        if user_turn_right:
            user_car.turn(1)
        if user_turn_left:
            user_car.turn(-1)

        framerate = clock.get_fps()
        framerate_label = font.render("FPS: ".join([str(framerate)]), 1, pygame.color.THECOLORS["black"])
        screen.blit(framerate_label, (0,0))
        
        user_car.draw(screen)
        user_car.move()
       
        track.draw(screen) 
       
        pygame.display.flip()
        clock.tick(50)
 
if __name__ == "__main__":
    sys.exit(main())
