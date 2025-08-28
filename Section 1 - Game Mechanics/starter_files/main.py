import csv

import pygame

import constants
from character import Character
from constants import SCREEN_WIDTH
from items import Item
from weapon import Weapon
from world import World

pygame.init()


#initialising screen
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

#screen name
pygame.display.set_caption("Dungeon Crawler")

#system clock for frame rate
clock = pygame.time.Clock()

#define game variables
level = 1
screen_scroll = [ 0, 0]

#define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

#scale images helper function
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, ((w * scale), (h * scale)))

#load heart images
heart_empty = scale_img(pygame.image.load('assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load('assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load('assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)

#load coin images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f'assets/images/items/coin_f{x}.png').convert_alpha(),constants.ITEM_SCALE)
    coin_images.append(img)

#load health potion
red_potion = scale_img(pygame.image.load(f'assets/images/items/potion_red.png').convert_alpha(),constants.POTION_SCALE)

#grouping these to make code easier to pass through functions
item_images = [coin_images, [red_potion]]

#load weapon images
bow_image = scale_img(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.WEAPON_SCALE)

#load tile map images
tile_list = []
for i in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f'assets/images/tiles/{i}.png').convert_alpha()
    tile_image = scale_img(tile_image, constants.SCALE)
    tile_list.append(tile_image)

#loading in all character images
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]

animation_types = ["idle", "run"]
for mob in mob_types:
    #loading in images
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#function for outputting text onto screen
def draw_text(text, font, x, y, color):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))

#function for displaying game info
def draw_info():
    #game info header
    pygame.draw.rect(screen, constants.GAME_INFO_PANEL, (0,0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0,50), (constants.SCREEN_WIDTH, 50))

    #draw lives
    half_heart_drawn = False
    for x in range(5):
        if player.health >= ((x + 1) * 20):
            screen.blit(heart_full, (10 + x * 50, 0))
        elif (player.health % 20 > 0) and not half_heart_drawn:
            screen.blit(heart_half, (10 + x * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + x * 50, 0))

    #level
    draw_text("LEVEL: " + str(level), font, 3 * (constants.SCREEN_WIDTH / 5) , 15, constants.WHITE)

    #show score
    draw_text(f"X{player.score}", font, SCREEN_WIDTH - 100 , 15 , constants.WHITE)


#create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
#load in levels and create world
with open(f"levels/level{level}_data.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

#damage text class
class DamageText(pygame.sprite.Sprite):

    def __init__(self, x, y, damage_value, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage_value), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, screen_scroll):
        #reposition damage text according to screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        #move damage text up
        self.rect.y -= 3.5
        #delete text after a few seconds
        self.counter += 1
        if self.counter >= 45:
            self.kill()

#create player
player = world.player

#create player's weapon
bow = Weapon(bow_image, arrow_image)

#extract enemy list from world data
enemy_list = world.character_list

#create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

#creating item instances
score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)

#add items from level data
for item in world.item_list:
    item_group.add(item)


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
    screen_scroll = player.move( dx, dy, world.obstacle_tiles)
    world.update(screen_scroll)


    #update all objects
    for enemy in enemy_list:
        enemy.ai(screen_scroll)
        enemy.update()
    player.update()
    #updating player weapon
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, enemy_list, world.obstacle_tiles)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, damage, constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update(screen_scroll)
    item_group.update(screen_scroll, player)

    #draw objects on screen
    world.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)

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