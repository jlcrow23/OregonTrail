# Import and initialize the pygame library
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import*
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
        
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting postion is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        
    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        
# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init() 
       
# Setup the clock for a decent framrate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for postion updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Music from #Uppbeat (free for Creators!):
# https://uppbeat.io/t/kevin-macleod/pookatori-and-friends
# License code: PUMBXXOL17SW3WTW
pygame.mixer.music.load("GameMusic.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == pygame.KEYDOWN:
            # Was it the escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
                
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
            
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
            
# Get the set of keys pressed and check for user input
pressed_keys = pygame.key.get_focused()

# Update the player sprite based on user keypress
player.update(pressed_keys)

# Update enemy position
enemies.update()
clouds.update()

# Fill the screen with white
# screen.fill((255, 255, 255))

# Fill the screen with black
# screen.fill((0, 0, 0))

# Fill the screen with skyblue
screen.fill((135, 206, 250))

# Draw all sprites
for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)
    
# Check if any enemies have collided with the player
if pygame.sprite.spritecollide(player, enemies):
    # If so, then remove the player and stop the loop
    player.kill()
    
    # Stop any mocing sounds and play the collision sound
    move_up_sound.stop()
    move_down_sound.stop()
    collision_sound.play()
    running = False
    
# Flip everything to the display
pygame.display.flip()

# Ensure program maintains a rate of 30 frames per second
clock.tick(30)

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()

# Create a surface and pass in a tuple containing its length and width
# surf = pygame.Surface((50, 50))

# Give the surface a color to seperate it from the background
# surf.fill((0, 0, 0))
# rect = surf.get_rect()

# Put the center of surf at the center of the display
# surf_center = (
#     (SCREEN_WIDTH-surf.get_width())/2,
#     (SCREEN_HEIGHT-surf.get_height())/2
# )

# This line says "Draw surf onto the screen at the center"
# screen.blit(surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# Draw surf at the new coordinates
# screen.blit(surf, surf_center)

# Draw the player on the screen
# screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
# screen.blit(player.surf, player.rect)

# Update the diplay
# pygame.display.flip()

