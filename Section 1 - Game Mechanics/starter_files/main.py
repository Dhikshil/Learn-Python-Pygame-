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

#scale images helper function
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, ((w * scale), (h * scale)))

#loading in images
animation_list = []
for i in range(4):
    img = pygame.image.load(f"assets/images/characters/elf/idle/{i}.png").convert_alpha()
    img = scale_img(img, constants.SCALE)
    animation_list.append(img)

#create player
player = Character(100,100, animation_list)

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
    if moving_right:
        dx = constants.SPEED
    if moving_left:
        dx = -constants.SPEED
    if moving_up:
        dy = -constants.SPEED
    if moving_down:
        dy = constants.SPEED
    
    #move player
    player.move( dx, dy)

    #update player images
    player.update()

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