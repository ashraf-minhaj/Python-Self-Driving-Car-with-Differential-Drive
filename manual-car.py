""" Car simulation with Python

 author: ashraf minhaj
 mail  : ashraf_minhaj@yahoo.com
"""

import pygame
import math

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
        pygame.display.set_caption("Differential Drive Car Simulation")
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
        screen.blit(self.rotated, self)

    def move(self, dt, event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    #self.velocity_l += 0.001*self.meter2pixel
                    self.velocity_r -= 0.002*self.meter2pixel

                if event.key == pygame.K_LEFT:
                    self.velocity_l -= 0.002*self.meter2pixel
                    #self.velocity_r += 0.001*self.meter2pixel

                if event.key == pygame.K_UP:
                    self.velocity_l += 0.001*self.meter2pixel
                    self.velocity_r += 0.001*self.meter2pixel
                    self.last_forward_velocity += 0.001*self.meter2pixel

                if event.key == pygame.K_DOWN:
                    self.velocity_l -= 0.003*self.meter2pixel
                    self.velocity_r -= 0.003*self.meter2pixel
                    self.last_forward_velocity -= 0.003*self.meter2pixel

                if event.key == pygame.K_e:
                    self.velocity_l = 0.00
                    self.velocity_r = 0.00
        else:
            diff = self.velocity_l - self.velocity_r
            print('Last Forward Velocity', self.last_forward_velocity, "Difference: ", diff, "Left ", self.velocity_l, "Right ", self.velocity_r)

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

        


# variables
dimension = (520, 1300)  # game dimension
start = (200, 200)       # start position of the car
running = True           # running or not
dt = 0
lasttime = pygame.time.get_ticks()

# init things here
pygame.init()
pygame.key.set_repeat(100)
environment = Environment(dimension, 'resources/bg1.jpg')
car = Car(start, 'resources/car.png', 0.01*3779.52)


# simulation loop
while running:
    # check for keyboard input
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        
        car.move(dt, event)

    dt = (pygame.time.get_ticks()-lasttime)/1000
    lasttime = pygame.time.get_ticks()

    pygame.display.update()
    environment.add_bg()
    car.move(dt)
    car.draw(environment.screen)
