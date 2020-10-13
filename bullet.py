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
        self.rect = py.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value. 
        self.y = float(self.rect.y)

    def update(self):
        # Moves the bullet up the screen and updates decimal position of bullet.
        self.y -= self.settings.bullet_speed

        # Updates the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        # Draw the bullet to the screen.
        py.draw.rect(self.screen, self.color, self.rect)