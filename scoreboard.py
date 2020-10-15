import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    # A class to report scoring information.

    def __init__(self, ai_game):
        # Initializes scorekeeping attributes.
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information: Color and Object. 
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        # Prepares the initial score images.
        # Turns text to be displayed into an image. 
        self.prep_score()
        # Prepares high score image. 
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_high_score(self):

        # Turns the high score into a rendered image.
        # Rounds high score to nearest 10 and formats it with commas.
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        # Generates image from the high score. 
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)

        # Centers the high score at the top of the screen. 
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):

        # Turns the level into a rendered image.
        level_str = str(self.stats.level)
        # Creates an image from the value soted in stats.level. 
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        # Sets image's right attribute to match the score's right attribute.
        self.level_rect.right = self.score_rect.right
        # Sets top attribute 10 pixels beneath the bottom of the score image to leave space between the score and the level. 
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_score(self):
        # Turns the score into a rendered image.
        # Rounds the value of stats score to the nearest 10 and store in rounded score.
        rounded_score = round(self.stats.score, -1)
        # Turns numerical value into a string.
        score_str = "{:,}".format(rounded_score)
        # Creates the image.
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)

        # Display the score at the top right of the screen.
        # Makes sure that score always lines up with the right side of the screen.
        self.score_rect = self.score_image.get_rect()
        # Sets its right edge 20 pixels from right edge of screen. 
        self.score_rect.right = self.screen_rect.right - 20
        # Places the top edge 20 pixels down from the top of the screen. 
        self.score_rect.top = 20

    def prep_ships(self):
        # Show how many ships are left. 
        # Creates an empty group to hold the ship instances.
        self.ships = Group()
        # Runs once for every ship the player has left.  
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            # Sets the ship's x coord value so the ships appear next to each other with a 10 pixel margin on the left side.
            ship.rect.x = 10 + ship_number * ship.rect.width
            # Sets y coord vale 10 pixels from the top of the screen so the ships appear in upper left corner.
            ship.rect.y = 10
            # Adds each new ship to the group of ships. 
            self.ships.add(ship)


    def show_score(self):
        # Draws the scores, levels, and ships to the screen. 
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):

        # Checks to see if there is a new high score.
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()