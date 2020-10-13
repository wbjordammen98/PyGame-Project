import sys
import pygame as py
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    # Overall class to manage game assets and behavior.

    def __init__(self):

        # Initialize the game, and create game resources.
        py.init()
        self.settings = Settings()
        self.screen = py.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = py.display.set_mode((0,0), py.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        py.display.set_caption("Alien Invasion")

        # Import the ship into the game. 
        self.ship = Ship(self)
        self.bullets = py.sprite.Group()
        self.aliens = py.sprite.Group()

        self._create_fleet()

        # Sets the background color
        self.bg_color = (230,230,230)

    def _create_fleet(self):
        # Creates fleet of aliens.

        # Creates an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determines the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Creates the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number)

    def _create_alien(self,alien_number):
        # Creates an alien and places it in the first row.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def run_game(self):

        # Start the game's main loop. 
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _update_bullets(self):
        self.bullets.update()

        # Gets rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

    def _check_events(self):
        # Watches for keyboard and mouse events.
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()

            elif event.type == py.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == py.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == py.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == py.K_LEFT:
            self.ship.moving_left = True
        elif event.key == py.K_q:
            sys.exit()
        elif event.key == py.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        if event.key == py.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == py.K_LEFT:
            self.ship.moving_left = False
                # Moves the ship to the right.
            self.ship.rect.x += 1

    def _fire_bullet(self):
        # Creates a new bullet and adds it to the bullets group.
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
    def _update_screen(self):
        # Updates images on the screen during each pass through the loop, and flips to the new screen.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        py.display.flip()

if __name__ == '__main__':
    # Makes a game instance, and runs the game.
    ai = AlienInvasion()
    ai.run_game()