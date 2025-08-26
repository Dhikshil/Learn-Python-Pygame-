import pygame
import math

import constants

class Character():
    def __init__(self, x, y, animation_list):
        self.flip = False
        self.frameIndex = 0
        self.action = 0 #action 0 means idle; action 1 is running
        self.running = False
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)
        self.image = animation_list[self.action][self.frameIndex]
        self.animation_list = animation_list

    def move(self, dx, dy):
        #checking if player is running
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True

        #check and control player and image direction
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        #controlling diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        animation_cooldown = 70

        #check action being performed by player
        if self.running == True:
            self.update_action(1) #1 means player is running
        else:
            self.update_action(0) #0 means player is idle

        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frameIndex]

        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frameIndex += 1
            self.update_time = pygame.time.get_ticks()

        #check if animation has finished
        if self.frameIndex >= len(self.animation_list[self.action]):
            self.frameIndex = 0

    def update_action(self, new_action):
        #checking if the new action is different to the previous action
        if new_action != self.action:
            self.action = new_action
            #reset the animation settings
            self.frameIndex = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        #flip direction if player changes direction
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.WHITE, self.rect, 1)