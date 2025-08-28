import pygame
import math

import constants



class Character():
    def __init__(self, x, y, mob_animations, character_type, health, boss, size):
        self.character_type = character_type
        self.score = 0
        self.flip = False
        self.animation_list = mob_animations[character_type]
        self.frameIndex = 0
        self.action = 0 #action 0 means idle; action 1 is running
        self.running = False
        self.health = health
        self.alive = True
        self.boss = boss
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.stunned = False

        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)
        self.image = self.animation_list[self.action][self.frameIndex]


    def move(self, dx, dy, obstacle_tiles):
        screen_scroll = [ 0, 0]

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

        #check for collision with walls
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            #check for obstacle collision
            if obstacle[1].colliderect(self.rect):
                #check which side collision is from
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right

        self.rect.y += dy
        for obstacle in obstacle_tiles:
            # check for obstacle collision
            if obstacle[1].colliderect(self.rect):
                # check which side collision is from
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom


        #logic only applicable to player
        if self.character_type == 0:
            #update scroll based on player position
            #move camera left and right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD):
                screen_scroll[0] = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD
            if self.rect.left < constants.SCROLL_THRESHOLD:
                screen_scroll[0] = constants.SCROLL_THRESHOLD - self.rect.left
                self.rect.left = constants.SCROLL_THRESHOLD
            # move camera up and down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD):
                screen_scroll [ 1 ] = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD
            if self.rect.top < constants.SCROLL_THRESHOLD :
                screen_scroll [ 1 ] = constants.SCROLL_THRESHOLD - self.rect.top
                self.rect.top = constants.SCROLL_THRESHOLD

        return screen_scroll

    def ai(self, screen_scroll, obstacle_tiles, player ):#
        ai_dx = 0
        ai_dy = 0
        clipped_line = ()
        stun_cooldown = 100

        #reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        #create a line of sight from player to enemy
        line_of_sight = ((self.rect.centerx ,self.rect.centery), (player.rect.centerx ,player.rect.centery))
        #check if line of sight passes through an obstacle tile
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        #check distance to player
        dist = math.sqrt((self.rect.centerx - player.rect.centerx)**2 + (self.rect.centery - player.rect.centery)**2)
        if constants.RANGE_MIN < dist < constants.RANGE_MAX and not clipped_line:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = constants.ENEMY_SPEED

            if self.rect.centery > player.rect.centery:
                ai_dy = -constants.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = constants.ENEMY_SPEED

        if self.alive:
            if not self.stunned:
                #move towards player
                self.move(ai_dx, ai_dy, obstacle_tiles)
                #attack player
                if dist <= constants.ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()

            #check if hit
            if self.hit:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.update_action(0)

            if (pygame.time.get_ticks() - self.last_hit) >= stun_cooldown:
                self.stunned = False


    def update(self):

        animation_cooldown = 70
        hit_cooldown = 1000

        #check if character is still alive
        if self.health <= 0:
            self.health = 0
            self.alive = False

        #rest player taking hit
        if self.character_type == 0:
            if self.hit == True and  (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                self.hit = False


        #check action being performed by player
        if self.running:
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
        if self.character_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
        else:
            surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.WHITE, self.rect, 1)