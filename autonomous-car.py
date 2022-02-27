""" Car simulation with Python

 author: ashraf minhaj
 mail  : ashraf_minhaj@yahoo.com
"""

from turtle import right
import pygame
import math
import numpy as np

class Environment:
    def __init__(self, dimensions, bg):
        # color variables
        self.black  = (0, 0, 0)
        self.white  = (255, 255, 255)
        self.green  = (0, 255, 0)
        self.blue   = (0, 0, 255)
        self.red    = (255, 0, 0)
        self.yellow = (255, 255, 0)

        # screen dimensions
        self.height = dimensions[0]
        self.width  = dimensions[1]

        # background
        self.bg_img = bg

        # window settings
        pygame.display.set_caption("2D autonomous Car with Differential Drive")
        self.screen = pygame.display.set_mode((self.width, self.height))

    def add_bg(self):
        self.bg = pygame.image.load(self.bg_img)
        #self.rect = self.bg.get_rect()
        self.screen.blit(self.bg, (0, 0))

class Car:
    def __init__(self, startpos, car_img, width):
        # variables
        self.meter2pixel = 3779.52

        self.w          = width
        self.x          = startpos[0]
        self.y          = startpos[1]
        self.theta      = 0                      # heading angle
        self.velocity_l = 0.00*self.meter2pixel  # m/s
        self.velocity_r = 0.00*self.meter2pixel
        self.min_speed  = 0.00*self.meter2pixel
        self.max_speed  = 0.02*self.meter2pixel

        self.last_forward_velocity = 0
        
        # image
        self.image = pygame.image.load(car_img)
        self.rotated = self.image
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        self.screen = screen
        screen.blit(self.rotated, self)
    

    def control_movement(self, dt, event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.move_right()

                if event.key == pygame.K_LEFT:
                    self.move_left()

                if event.key == pygame.K_UP:
                    self.move_forward()

                if event.key == pygame.K_DOWN:
                    self.move_backward()

                if event.key == pygame.K_e:
                    self.velocity_l = 0.00
                    self.velocity_r = 0.00
        else:
            diff = self.velocity_l - self.velocity_r
            print('[Main Control Val] Theta', self.theta, 'Last F Vel', self.last_forward_velocity, "Diff: ", diff, "L", self.velocity_l, "R", self.velocity_r)
            print('[Robot coord]', self.x, self.y)

            if diff < -2 or diff > 2:
                if self.velocity_l < self.last_forward_velocity:
                    self.velocity_l += 0.3
                
                if self.velocity_l > self.last_forward_velocity:
                    self.velocity_l -= 0.3
                
                if self.velocity_r < self.last_forward_velocity:
                    self.velocity_r += 0.3

                if self.velocity_r > self.last_forward_velocity:
                    self.velocity_r -= 0.3
                
            elif diff > -1 or diff < 1:
                self.velocity_r = self.last_forward_velocity
                self.velocity_l = self.last_forward_velocity

        if self.velocity_l == self.velocity_r:
            self.last_forward_velocity = self.velocity_l

        # print('LastForwardVelocity', self.last_forward_velocity)

        self.x += ((self.velocity_l+self.velocity_r)/2)*math.cos(self.theta)*dt
        self.y -= ((self.velocity_l+self.velocity_r)/2)*math.sin(self.theta)*dt
        self.theta += (self.velocity_r-self.velocity_l)/self.w*dt

        self.rotated = pygame.transform.rotozoom(self.image, math.degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def move_left(self):
        self.velocity_l -= 0.002*self.meter2pixel
        #self.velocity_r += 0.001*self.meter2pixel

    def move_right(self):
        #self.velocity_l += 0.001*self.meter2pixel
        self.velocity_r -= 0.01*self.meter2pixel

    def move_forward(self):
        self.velocity_l += 0.001*self.meter2pixel
        self.velocity_r += 0.001*self.meter2pixel
        self.last_forward_velocity += 0.001*self.meter2pixel

    def move_backward(self):
        self.velocity_l -= 0.003*self.meter2pixel
        self.velocity_r -= 0.003*self.meter2pixel
        self.last_forward_velocity -= 0.003*self.meter2pixel

    def draw_sensors(self):
        # pygame.draw.circle(self.screen, (255, 0, 0), [self.x, self.y], 5, 5)
        self.sensor_pos = [[0,0], [0,0], [0, 0]]

        start_angle = self.theta - 30
        end_angle   = self.theta + 30
        # print(self.theta, start_angle, end_angle)

        self.p = self.x + 20*math.cos(self.theta)
        self.q = self.y - 20*math.sin(self.theta)
        pygame.draw.circle(self.screen, (255, 255, 0), [self.p, self.q], 5, 5)

        angles = np.linspace(start_angle, end_angle, 3, True)
        # angles = [-30, 0, 30]
        print('[angles]', angles)
        for i, angle in enumerate(angles):
            x2 = math.ceil(self.p + 25*math.cos(angle))
            y2 = math.ceil(self.q - 25*math.sin(angle))
            self.sensor_pos[i]=[x2, y2]
            # print(x2, y2)
            # draw sensors after getting the values, else they collide
            #pygame.draw.circle(self.screen, (255, 0, 0), [x2, y2], 5, 5)
            #pygame.draw.line(self.screen, (0, 0, 255), (p, q), (x2, y2))

        # print(self.sensor_pos)

    def detect_obstacle(self):
        # left = self.sensor_pos[0]
        # front = self.sensor_pos[1]
        # right = self.sensor_pos[2]
        print('[Sensor Pos] Front', self.sensor_pos[0], 'Right', self.sensor_pos[1], 'Left', self.sensor_pos[2])

        col_l = self.screen.get_at((self.sensor_pos[0][0], self.sensor_pos[0][1]))[:3]
        col_f = self.screen.get_at((self.sensor_pos[1][0], self.sensor_pos[1][1]))[:3]
        col_r = self.screen.get_at((self.sensor_pos[2][0], self.sensor_pos[2][1]))[:3]
        print('[sensor cols]', col_f, col_r, col_l)

        for sensor in self.sensor_pos:
            pygame.draw.circle(self.screen, (255, 0, 0), sensor, 5, 5)
            pygame.draw.line(self.screen, (0, 0, 255), (self.p, self.q), (sensor[0], sensor[1]))

        if col_f[0] == 0:
            self.move_right()
            # self.velocity_r = 0
            # self.velocity_l = 0
            # self.velocity_r = self.last_forward_velocity
            # self.velocity_l = self.last_forward_velocity
            # self.move_forward()

        


# variables
dimension = (520, 1300)  # game dimension
start = (200, 200)       # start position of the car
running = True           # running or not
dt = 0
lasttime = pygame.time.get_ticks()

# init things here
pygame.init()
pygame.key.set_repeat(100)
environment = Environment(dimension, 'resources/bg2.png')
car = Car(start, 'resources/car.png', 0.01*3779.52)


# simulation loop
while running:
    # check for keyboard input
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            running = False
        
        car.control_movement(dt, event)

    dt = (pygame.time.get_ticks()-lasttime)/1000
    lasttime = pygame.time.get_ticks()

    pygame.display.update()
    environment.add_bg()
    car.draw(environment.screen)
    car.control_movement(dt)
    car.draw_sensors()
    car.detect_obstacle()
