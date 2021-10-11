# Import the pygame module
import pygame

import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from pygame.sprite import Group

#Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT= 600

#Define a Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        #self.surf = pygame.Surface((75,25))
        self.surf = pygame.image.load("rocket.png").convert()
        #self.surf.fill((255,255,255))
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_a]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5,0)

        #Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#Define enemy object
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf = pygame.image.load("bullet.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        # self.surf = pygame.Surface((20,10))
        # self.surf.fill((255,200,200))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0,SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5,20)

    def update(self):
        #move the sprite based on speed
        self.rect.move_ip(-self.speed, 0)
        #remove the sprite when it passes the left edge of the screen
        if self.rect.right < 0:
            self.kill()

# Initialize pygame
pygame.init()

#Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#Create a custom event for addingg a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

#Instantiate the player
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Variable to keep the main loop running 
running = True

#main loop
while running:
    #Look at every event in the queue
    for event in pygame.event.get():
        #did the user hit a key?
        if event.type == KEYDOWN:
            #check for escape
            if event.key == K_ESCAPE:
                running = False

        # Was it the window close button?
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            #Create a new enemy and add it to spire groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    #Get all keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    #Update the player sprite based on kepresses
    player.update(pressed_keys)

    #Update enemy position
    enemies.update()

    #Fill the screnn with black
    screen.fill((0,0,0))

    # #Draw the player on the screen
    # screen.blit(player.surf, player.rect)

    #Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Collision detection
    if pygame.sprite.spritecollideany(player,enemies):
        #remove the player and stop the loop
        player.kill()
        running = False

    #Flip everything to the display
    pygame.display.flip()



