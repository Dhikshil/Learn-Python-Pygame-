import pygame
import constants
from character import Character

pygame.init()


#initialising screen
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

#screen name
pygame.display.set_caption("Dungeon Crawler")

#system clock for frame rate
clock = pygame.time.Clock()

#define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

player_image = pygame.image.load("assets/images/characters/elf/idle/0.png").convert_alpha()

#create player
player = Character(100,100, player_image)

#main game loop
run = True
while run:
    #control frame rate
    clock.tick(constants.FPS)

    #reset screen 
    screen.fill(constants.BG)

    #calculate player movement
    dx = 0
    dy = 0
    if moving_right == True:
        dx = constants.SPEED
    if moving_left == True:
        dx = -constants.SPEED
    if moving_up == True:
        dy = -constants.SPEED
    if moving_down == True:
        dy = constants.SPEED
    
    #move player
    player.move( dx, dy)

    #draw player on screen
    player.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_w:
                moving_up = True

        #take keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_w:
                moving_up = False
        

    pygame.display.update()

pygame.quit()