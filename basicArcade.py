# Import and initialize the pygame library
import pygame

# Import mixer for sounds
from pygame import mixer

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

#define fps/ frame rate
clock = pygame.time.Clock()
fps = 60

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jet Fighter Game')

# define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

# load sounds
explosion_fx = pygame.mixer.Sound('sounds/explosion.wav')
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound('sounds/explosion2.wav')
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound('sounds/laser.wav')

# game variables
alien_cooldown = 1000#bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0#0 is no game over, 1 means player has won, -1 means player has lost

# define colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
# background color
BG = (113, 205, 245)

# Fill the screen with skyblue
screen.fill(BG)

# function to create text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
# Player define

class Player(pygame.sprite.Sprite):
    def  __init__(self,  x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/jet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

        
    def update(self):
        # set movement speed
        speed = 8
        # set cooldown variable
        cooldown = 500 # milliseconds
        game_over = 0
        
        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top < 0:
            self.rect.x -= speed
            
        if key[pygame.K_DOWN] and self.rect.bottom > SCREEN_HEIGHT:
            self.rect.x += speed
            
        # get current time
        time_now = pygame.time.get_ticks()
        
        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.right)
            bullet_group.add(bullet)
            self.last_shot = time_now
            
        # update mask
        self.mask = pygame.mask.from_surface(self.image)
        
        # draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.centery + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.centery + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over
    
# Create bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.centery = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, enemies, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            
# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('images/alien' + str(random.randint(1, 5)) + '.png')
        self.rect = self.image.get_rect(
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
     
# Create Enemy bullet class
class Enemy_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/alien_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.centery = [x, y]
        
    def update(self):
        self.rect.y += 2
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.spretir.collide_mask):
            self.kill()
            explosion2_fx.play()
            #reduce spaceship health
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)

#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f'images/exp{num}.png')
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			#add the image to the list
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0


	def update(self):
		explosion_speed = 3
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, delete explosion
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()
            
# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load('images/cloud.png').convert_alpha()
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
            
            
            

# Create a custom event for adding a new enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)



# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for postion updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

#create player
spaceship = Player(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100, 3)
spaceship_group.add(spaceship)


# Variable to keep the main loop running
running = True

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
            
    if countdown > 0:
        draw_text('GET READY!', font40, white, int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 + 50))
        draw_text(str(countdown), font40, white, int(SCREEN_WIDTH / 2 - 10), int(SCREEN_HEIGHT / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
            
    if countdown == 0:
        # create random alien bullets
        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5:
            attacking_alien = random.choice(enemies.sprites())
            alien_bullet = Enemy_Bullets(attacking_alien.rect.right, attacking_alien.rect.left)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now
            
        if game_over == 0:
			#update spaceship
            game_over = spaceship.update()

			#update sprite groups
            bullet_group.update()
            enemies.update()
            alien_bullet_group.update()
        else:
            if game_over == -1:
                draw_text('GAME OVER!', font40, white, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))
            if game_over == 1:
                draw_text('YOU WIN!', font40, white, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))

# Update the player sprite based on user keypress
spaceship.update()

# Update enemy position
enemies.update()
clouds.update()
explosion_group.update()

# Draw all sprites
for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)
    
# Check if any enemies have collided with the player
if pygame.sprite.spritecollide(spaceship, enemies):
    # If so, then remove the player and stop the loop
    spaceship.kill()
    
    running = False
    
# Flip everything to the display
pygame.display.flip()

# Ensure program maintains a rate of 30 frames per second
clock.tick(30)

pygame.display.update()

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()