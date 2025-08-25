import pygame
import math

import constants

class Character():
    def __init__(self, x, y, player_image):
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)
        self.image = player_image

    def move(self, dx, dy):
        #controlling diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, constants.WHITE, self.rect, 1)