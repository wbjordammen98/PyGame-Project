import pygame
from pygame.sprite import Sprite

# Imports sprite for Ship to inherit.
class Ship(Sprite):
    # A class to manage the ship.

    # Creates settings attribute for Ship to be used in update(). 
    def __init__(self, ai_game):
        # Initialize the ship and set its starting position.
        # Calls super() the beginning of __init__().
        super().__init__()
        # Assigns the screen to an attribute of Ship class to easily access methods its methods.
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # Accesses the screen's rect attribute to place the ship in the current location on the screen. 
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Stores a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags for movement attributes, moves ship to right if True, moves if to left if True.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Updates the ship's position based on the movement flags.

        # If this value is less than the value returned by self.screen rect.right, the ship hasn't reached the right edge.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # Value is adjusted by the amount stored in settings.ship_speed.
            self.x += self.settings.ship_speed
        # Signifies that the ship hasn't reached the left edge of the screen. 
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Updates rect object form self.x new value which controls position of the ship.
        self.rect.x = self.x

    def blitme(self):
        # Draws the ship at its current location on the screen specified by self.rect.

        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # Center the ship on the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

