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
        # Imports Settings class, thens creates an instance of said class and assigns to self.settings.
        self.settings = Settings()
        # Creates a screen and implements the settings of the height and width attributes of self.settings.
        self.screen = py.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # While creating the screen surface, this passes a size of (0, 0) and the parameter game.
        self.screen = py.display.set_mode((0,0), py.FULLSCREEN)
        # Updates the settings object via the width and height attributes of the screen. 
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        py.display.set_caption("Alien Invasion")

        # Creates an instance to store game statistics and creates the scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Imports the ship into the game.
        # The parameter gives Ship's access to the game's resources such as the screen object. 
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

            # Reduces number of ships_left, and updates scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Gets rid of any remaining aliens and bullets in their respective groups.
            self.aliens.empty()
            self.bullets.empty()

            # Creates a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pauses unitl updates are made to all game elements.
            sleep(0.5)
        else:
            self.stats.game_active = False
            py.mouse.set_visible(True)

    def _create_fleet(self):
        # Creates fleet of aliens.

        # Creates an alien.
        alien = Alien(self)
        # Gets alien's width and height from its rect attribute to store into its repective values.
        alien_width, alien_height = alien.rect.size
        # Calculates horizontal space availble for the aliens to fit into.
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determines the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        # Calculates the number of rows we can fit on the screen.
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Creates the full fleet of aliens.
        for row_number in range(number_rows):
            # Sets up a loop that counts the number of aliens needed to make. 
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self,alien_number,row_number):
        # Creates an alien and places it in the first row.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Creates a new alien and sets its x-coordinate value to place in row.
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        # Changes an alien's y-coord value when it is not in the first row. 
        # Starts with one alien's height to create empty space at the top of the screen. 
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):

        # Start the game's main loop. 
        while True:
            # Calls the method from inside the While loop in run_game.
            self._check_events()

            if self.stats.game_active:

                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            # Gets rid of bullets that have disappered.
            # Copy method enables to modifiy bullets inside the loop.
            for bullet in self.bullets.copy():
                # Checks to see if each bullet has disappeared of the top of the screen.
                if bullet.rect.bottom <= 0:
                    # If so, removes from bullets. 
                    self.bullets.remove(bullet)
            # Shows how many bullets currently exist in game and verifies that they're being deleted of the screen.
            print(len(self.bullets))

            
            self._update_screen()

    def _update_bullets(self):
        # Calls update on group which automatically calls update() for each sprite in group.
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
        # Loops through all values of the dictionary.
        if collisions:
            for aliens in collisions.values():
                # Multiples value of each alien by the number of aliens in each list and adds to current stuff. 
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        # Checks whether or not the aliens group is empty. 
        if not self.aliens:
            # Destroys existing bullets sprites.  
            self.bullets.empty()
            # Creates new fleet.
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
        # Watches for keyboard and mouse events and responds to them.
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            # Responds when Pygame detects a keydown event.
            elif event.type == py.KEYDOWN:
                self._check_keydown_events(event)
            # Resonds to keyup events , when player releases right arrow key moving right is set to True. 
            elif event.type == py.KEYUP:
                self._check_keyup_events(event)
            # Detects for event when the player clicks anywhere on the screen. 
            elif event.type == py.MOUSEBUTTONDOWN:
                # Returns tuple containing the cursor's x and y coords when mouse button is clicked.
                mouse_pos = py.mouse.get_pos()
                # Sends values from mouse_pos to method. 
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        # Starts a new game when the player clicks 'Play'.

        # The flag button_clicked stores a True or False value and restarts only if Play is clicked and game is not active. 
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # Checks whether the point of the mouse click overlaps the region defined by the Play button's rect.
        if button_clicked and not self.stats.game_active:

            # Resets the game settings.
            self.settings.initialize_dynamic_settings()

            # Resets the game stats and gives player three new ships.  
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Gets rid of any remaining aliens and bullets from their respective groups. 
            self.aliens.empty()
            self.bullets.empty()

            # Creates a new fleet and centers the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hides the mouse cursor.
            py.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        # Checks whether the right arrow key is pressed. 
        if event.key == py.K_RIGHT:
            # Modifies how the game responds when the player presses right.
            self.ship.moving_right = True
        elif event.key == py.K_LEFT:
            self.ship.moving_left = True
        elif event.key == py.K_q:
            sys.exit()
        # Calls on fire bullet when spacebar is pressed.    
        elif event.key == py.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        if event.key == py.K_RIGHT:
            # Adds moving right attribute in the init method at initially False. 
            self.ship.moving_right = False
        elif event.key == py.K_LEFT:
            self.ship.moving_left = False
                # Moves the ship to the right.
            self.ship.rect.x += 1

    def _fire_bullet(self):
        # Creates a new bullet and adds it to the bullets group.
        if len(self.bullets) < self.settings.bullets_allowed:
            # Creates instance of new bullet.
            new_bullet = Bullet(self)
            # Adds new bullet to the group bullets.
            self.bullets.add(new_bullet)

    def _check_fleet_edges(self):
        # Responds appropriately if any aliens have reached an edge.
        # Loops through fleet and call check_edges on each alien. 
        for alien in self.aliens.sprites():
            if alien.check_edges():
                # Detects if alien is at the edge and changes the fleet's direction.
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        # Checks if any aliens have reached the bottom of the screen.
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            # Signifies that an alien has reached the bottom. 
            if alien.rect.bottom >= screen_rect.bottom:
                # Treats this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        # Drop the entire fleet and change the fleet's direction.
        for alien in self.aliens.sprites():
            # Loops through all aliens and drops each one.
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _update_screen(self):
        # Updates images on the screen during each pass through the loop, and flips to the new screen.
        self.screen.fill(self.settings.bg_color)
        # Draws ship on the screen to appear on top of the backgorund.
        self.ship.blitme()
        # Draws all fired bullets on to the screen by looping through the sprites in Bullets and calls draw_bullet on each one. 
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