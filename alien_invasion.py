import sys
from time import sleep
import pygame as py
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    # Overall class to manage game assets and behavior.

    def __init__(self):

        # Initializes the game, and creates the game's resources.
        py.init()
        self.settings = Settings()
        self.screen = py.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = py.display.set_mode((0,0), py.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        py.display.set_caption("Alien Invasion")

        # Creates an instance to store game statistics and creates the scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Imports the ship into the game. 
        self.ship = Ship(self)
        self.bullets = py.sprite.Group()
        self.aliens = py.sprite.Group()

        self._create_fleet()

        # Makes the 'Play' button.
        self.play_button = Button(self, "Play") 

        # Sets the background color
        self.bg_color = (230,230,230)

    def _ship_hit(self):
        # Responds to the ship being hit by an alien.
        if self.stats.ships_left > 0:

            # Decrements ships_left, and updates scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Gets rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.aliens.empty()

            # Creates a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            py.mouse.set_visible(True)

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
                self._create_alien(alien_number, row_number)

    def _create_alien(self,alien_number,row_number):
        # Creates an alien and places it in the first row.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):

        # Start the game's main loop. 
        while True:
            self._check_events()

            if self.stats.game_active:

                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))

            
            self._update_screen()

    def _update_bullets(self):
        self.bullets.update()

        # Gets rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Responds to bullet-alien collisions

        # Checks for any bullets that have hit aliens and gets rid of bullet and alien.
        collisions = py.sprite.groupcollide(self.bullets,self.aliens,True,True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroys existing bullets and creates new fleet.
            self.bullets.empty()
            self._create_fleet() 
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        # Checks to see if the fleet is at an edge, then updates the positions of all aliens in the fleet.
        self._check_fleet_edges()
        self.aliens.update()

        # Looks for alien-ship collisions.
        if py.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            print("Ship Hit!!!")

        # Looks for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_events(self):
        # Watches for keyboard and mouse events.
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()

            elif event.type == py.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == py.KEYUP:
                self._check_keyup_events(event)

            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_pos = py.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        # Starts a new game when the player clicks 'Play'.

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            # Resets the game settings.
            self.settings.initialize_dynamic_settings()

            # Resets the game stats.  
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets. 
            self.aliens.empty()
            self.bullets.empty()

            # Creates a new fleet and centers the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hides the mouse cursor.
            py.mouse.set_visible(False)

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

    def _check_fleet_edges(self):
        # Responds appropriately if nay aliens have reached an edge.
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        # Checks if any aliens have reached the bottom of the screen.
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treats this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        # Drop the entire fleet and change the fleet's direction.
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _update_screen(self):
        # Updates images on the screen during each pass through the loop, and flips to the new screen.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draws the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        py.display.flip()

if __name__ == '__main__':
    # Makes a game instance, and runs the game.
    ai = AlienInvasion()
    ai.run_game()