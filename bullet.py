import pygame as py
from pygame.sprite import Sprite

class Bullet(Sprite):
    # A Class to manage bullets fired from the ship.

    def __init__(self, ai_game):

        # Creates a bullet object at the ship's current position.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Creates a bullet rect at (0,0) and then set correct position.
        # Builds rect from scratch using the pygame Rect class.
        self.rect = py.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        # This makes the bullet emerge from top of the ship.
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value to be used for adjusting its speed. 
        self.y = float(self.rect.y)

    def update(self):
        # Moves the bullet up the screen and updates decimal position of bullet.
        self.y -= self.settings.bullet_speed

        # Updates the rect position with value from self.y.
        self.rect.y = self.y

    def draw_bullet(self):
        # Draws the bullet to the screen.
        py.draw.rect(self.screen, self.color, self.rect)