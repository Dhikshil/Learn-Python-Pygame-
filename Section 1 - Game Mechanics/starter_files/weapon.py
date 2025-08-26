import pygame
import math

class Weapon():
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.arrow_image = arrow_image

    def update(self, player):
        arrow = None

        self.rect.center = player.rect.center
        #angle bow to direction of mouse
        mouse_pos = pygame.mouse.get_pos()
        x_dist = mouse_pos[0] - self.rect.centerx
        y_dist = -(mouse_pos[1] - self.rect.centery)#negative because pygame has a negative y-axis
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        #get mouse clicks to register
        if pygame.mouse.get_pressed()[0]: #0 is left click button, 1 is middle click/scroll wheel, 2 is right click
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, (self.rect.centerx - int(self.image.get_width() / 2), (self.rect.centery - int(self.image.get_height() / 2))))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
