import pygame as py
from pygame.sprite import Sprite

class Alien(Sprite):
    # A class to represent a single alien in the fleet.

    def __init__(self,ai_game):
        # Initializes the alien and set its starting postion.

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = py.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        # Adds a space to the left of it that's equal to the alien's width and a space above it. 
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Stores and tracks the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        # Returns True if alien is at edge of screen.
        screen_rect = self.screen.get_rect()
        # Signifies that the alien is at the left edge if its left value is less than equal to 0.
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # Moves the alien to the right and tracks its exact position.
        # Allows motion to left or right by multiplying the alien's speed by the value of fleet_direction. 
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        # Uses value of self.x to update the position of the alien's rect.
        self.rect.x = self.x