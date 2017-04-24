import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# --- Classes


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("villain.png").convert()


        self.rect = self.image.get_rect()
    def update(self):
        if self.rect.x < 680 and self.rect.y % 2 != 0:
            self.rect.x += 5
        elif self.rect.x >= 680:
            self.rect.y += 25
            self.rect.x -= 5
        elif self.rect.x > 5 and self.rect.y % 2 == 0:
            self.rect.x -= 5
        elif self.rect.x <= 5:
            self.rect.y += 25



class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("player2.png").convert()



        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0]


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()



    def update(self):
        """ Move the bullet. """
        self.rect.y -= 5

# --- Create the window

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# ------ Sound Effects
click_sound = pygame.mixer.Sound("laser5.ogg")
death_sound = pygame.mixer.Sound("atari_boom.wav")
# --- Sprite lists

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

player_list = pygame.sprite.Group()
# --- Create the sprites
for i in range (1):
    player = Player()
    all_sprites_list.add(player)
    player_list.add(player)

for i in range(20):
    # This represents a block
    block = Block(BLUE)

    # Set a random location for the block
    block.rect.x = 30 * i
    block.rect.y = 25

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Create a red player block

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0
player.rect.y = 375
# -------- Main Program Loop -----------





while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button

            bullet = Bullet()

            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x + 13
            bullet.rect.y = player.rect.y


            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
            click_sound.play()
            print ("User left-clicked")
            print (bullet.rect.y)

    # --- Game logic

    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            death_sound.play()
            print(score)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    for player in player_list:

        player_hit_list = pygame.sprite.spritecollide(player, block_list, True)
        print (player_hit_list)
        for block in player_hit_list:
            player_list.remove(player)
            all_sprites_list.remove(player)
            death_sound.play()



    # --- Draw a frame
    background_image = pygame.image.load("saturn_family1.jpg").convert()
    screen.blit(background_image, [0,0])
    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render("Score: %s" %(score), True, WHITE)
    screen.blit(text, [250, 250])
    # Clear the screen


    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)

pygame.quit()
