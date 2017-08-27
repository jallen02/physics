import sys, random, math
import pygame
from pygame.locals import *
from shapely.geometry import LineString
import network as nnet

height = 1100
width = 1100
friction = .2

def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end

    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points 

def line_intersect(l1_start, l1_end, l2_start, l2_end):
    line1 = LineString([l1_start, l1_end])
    line2 = LineString([l2_start, l2_end])
    intersect = line1.intersection(line2)
    if intersect.type == "Point":
        return (intersect.x, intersect.y)
    return None
   
    
class Wall: 
    def __init__(self, a:(int, int), b:(int, int)): 
        self.line = get_line(a, b)
        self.a = a
        self.b = b

    def draw(self, screen, color):
        pygame.draw.line(screen, color, self.a, self.b)

class Track: 
    def __init__(self, track_info:str, color:(int,int,int)): 
        self.sections = [[]] 
        self.set_walls(track_info) 
        self.color = color 

    def set_walls(self, track_info:str):
        points = open(track_info).readlines()
        last_point = None
        for point in points:
            if point.isspace():
                self.sections.append([])
                last_point = None
            elif point.startswith("start_point"):
                self.start_point = (int(point.split()[1]), \
                                    int(point.split()[2]))
            elif point.startswith("start_angle"):
                self.start_angle = int(point.split()[1])
            else:
                point = point.split()
                point = (int(point[0]), int(point[1]))
                if last_point != None:
                    self.sections[-1].append(Wall(point, last_point))
                last_point = point
            
    def draw(self, screen):
        for section in self.sections:
            for wall in section:
                wall.draw(screen, self.color)
 
class Sight:
    def __init__(self, angle, track, origin):
        self.angle = angle
        self.track = track
        self.origin = origin
        self.endpoint = (0,0)
        self.length = 0
    
    def extend_los(self):
        x_incr = math.cos(math.radians(self.angle))*width
        y_incr = math.sin(math.radians(self.angle))*height
        endpoint = (self.origin[0] + x_incr, self.origin[1] + y_incr)
        points = []

        for section in self.track.sections:
            for wall in section:
                p = line_intersect(self.origin, endpoint, wall.a, wall.b)
                if p != None:
                    points.append(p)
        minlength = math.pow(height,2) + math.pow(width, 2)
        for point in points:
            length = math.sqrt(math.pow(point[0] - self.origin[0], 2) + math.pow(point[1] - self.origin[1], 2))
            if length < minlength:
                endpoint = point
                minlength = length
        self.endpoint = endpoint
        self.length = minlength

    def draw(self, screen, color):
        pygame.draw.line(screen, color, self.origin, self.endpoint)
        pygame.draw.circle(screen, color, (int(self.endpoint[0]), int(self.endpoint[1])), 10)

class Car:
    def __init__(self, size:(int,int), color:(int, int, int), \
                 acc_rate:float, brake_rate:float, turn_rate:float, \
                 max_speed:float, track:Track, network:nnet.Network = None):

        self.image = pygame.Surface(size)
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.angle = track.start_angle
        self.speed = 0
        self.acc_rate = acc_rate
        self.turn_rate = turn_rate
        self.brake_rate = brake_rate
        self.max_speed = max_speed
        self.pos = track.start_point
        self.color = color
        self.track = track
        self.distance = 0

        self.los = [Sight(self.angle + 45, track, self.pos), \
                    Sight(self.angle, track, self.pos), \
                    Sight(self.angle - 45, track, self.pos)]

        self.network = nnet.Network(4, 2, 8, 4)

    def move(self, usr = False):
        self.collision()
        if not usr:
            self.network.process_input([self.los[0].length, self.los[1].length, self.los[2].length, self.speed*10])
            self.network.propogate()
            result = self.network.max_output()
            if result == 0:
                self.accelerate()
            elif result == 1:
                self.brake()
            elif result == 2:
                self.turn(-1)
            elif result == 3:
                self.turn(1)

        x_incr = math.cos(math.radians(self.angle))
        y_incr = math.sin(math.radians(self.angle))
        x = self.pos[0] + (x_incr * self.speed)
        y = self.pos[1] + (y_incr * self.speed)
        self.distance += x_incr * self.speed + y_incr * self.speed
        self.pos = (x, y)
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.speed -= friction
        if self.speed < 0:
            self.speed = 0

        for sight in self.los:
            sight.origin = self.pos
            sight.extend_los()

    def turn(self, direction:float):
        self.angle += self.turn_rate*direction

        for sight in self.los:
            sight.angle += self.turn_rate*direction

    def accelerate(self):
        self.speed += self.acc_rate
        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def brake(self):
        self.speed -= self.brake_rate
        if (self.speed < 0):
            self.speed = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        for sight in self.los:
            sight.draw(screen, pygame.color.THECOLORS["lightgray"])

        self.network.draw(screen, (600, 100))
 
    def collision(self):
        for section in self.track.sections:
            for wall in section:
                for point in wall.line:
                    if self.rect.collidepoint(point):
                        self.collide()

    def collide(self):
        self.network.fitness = self.distance
        self.network.complete = True
        self.distance = 0
        self.speed = 0
        self.pos = self.track.start_point
        
        for sight in self.los:
            sight.angle -= self.track.start_angle + self.angle 

        self.angle = self.track.start_angle

def main():
    pygame.init()
    font = pygame.font.SysFont("monospace", 15)
    screen = pygame.display.set_mode((height, width))
    pygame.display.set_caption("Driiiiive!")
    clock = pygame.time.Clock()

    track = Track("track.txt", pygame.color.THECOLORS["black"])

    population_size = 20
    Car((10, 10), pygame.color.THECOLORS["blue"], .5, 1, 10, 10, track)


    #user_car = Car((10, 10), pygame.color.THECOLORS["blue"], .5, 1, 10, 10, track)
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
        ''' 
        if user_acc:
            user_car.accelerate()
        if user_brake:
            user_car.brake()
        if user_turn_right:
            user_car.turn(1)
        if user_turn_left:
            user_car.turn(-1)
        '''
        framerate = clock.get_fps()
        framerate_label = font.render("FPS: ".join([str(framerate)]), 1, pygame.color.THECOLORS["black"])
        screen.blit(framerate_label, (0,0))

        '''distance = user_car.distance
        distance_label = font.render("Distance".join([str(distance)]), 1, pygame.color.THECOLORS["black"])
        screen.blit(distance_label, (500, 0))
        '''
        
        #user_car.draw(screen)
        #user_car.move()
       
        track.draw(screen) 
       
        pygame.display.flip()
        clock.tick(50)
 
if __name__ == "__main__":
    sys.exit(main())
