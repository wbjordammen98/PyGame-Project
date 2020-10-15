Alien Inavasion PyGame Project Information Guide
""" Provides each function unique to its folder from the class."""

""" For more detail, look at the code."""

"""Folder 1: Alien Invasion"""

Class Alien Invasion:(Overall class to manage game assets and behavior. )

     def __init__(self): # Initializes the game, and creates the game's resources.

     def _ship_hit(self): Responds to the ship being hit by an alien.

     def _create_fleet(self): Creates fleet of aliens.

     def _create_alien(self,alien_number,row_number): Creates an alien and places it in the first row.

     def run_game(self): Start the game's main loop.
     
     def _update_bullets(self): Calls update on group which automatically calls update() for each sprite in group.

     def _check_bullet_alien_collisions(self):Responds to bullet-alien collisions

     def _update_aliens(self): Checks to see if the fleet is at an edge, then updates the positions of all aliens in the fleet.

     def _check_events(self):Watches for keyboard and mouse events and responds to them.

     def _check_play_button(self,mouse_pos): Starts a new game when the player clicks 'Play'.

     def _check_keydown_events(self, event):

     def _check_keyup_events(self, event):

     def _fire_bullet(self):

     def _check_fleet_edges(self): Responds appropriately if any aliens have reached an edge.

     def _check_aliens_bottom(self): Checks if any aliens have reached the bottom of the screen.

     def _change_fleet_direction(self): Drop the entire fleet and change the fleet's direction.

     def _update_screen(self): Updates images on the screen during each pass through the loop, and flips to the new screen.

     """ Folder 2: Alien """

Class Alien(Sprite):

    def __init__(self,ai_game): Initializes the alien and set its starting postion.

    def check_edges(self):

    def update(self): Moves the alien to the right and tracks its exact position.

    """ Folder 3: Bullet """

Class Bullet(Sprite): A Class to manage bullets fired from the ship.

    def __init__(self, ai_game):

    def update(self): Moves the bullet up the screen and updates decimal position of bullet.

    def draw_bullet(self): Draws the bullet to the screen.

    """ Folder 4: Button """

Class Button:

    def __init__(self,ai_game,msg): Initializes button attributes.

    def _prep_msg(self,msg): Turns msg into a rendered image.

    def draw_button(self):
        # Draw blank button and then draw message.

    """ Folder 5: Scoreboard """

Class Scoreboard: A class to report scoring information.

    def __init__(self, ai_game): Initializes scorekeeping attributes.

    def prep_high_score(self): Turns the high score into a rendered image.

    def prep_level(self):

    def prep_score(self): Turns the score into a rendered image.

    def prep_ships(self): Show how many ships are left. 

    def show_score(self): Draws the scores, levels, and ships to the screen.

    def check_high_score(self): Checks to see if there is a new high score.

    """ Folder 6: Settings """

Class Settings: Class that stores all settings for Alien Invasion.

    def __init__(self): Initializes the game's static settings.

    def initialize_dynamic_settings(self): Initializes settings that change throughout the game. 

    def increase_speed(self): Increases speed settings and alien point values.

    """ Folder 7 Ship  """

Class Ship(Sprite): Imports sprite for Ship to inherit. A class to manage the ship. 

    def __init__(self, ai_game): Initialize the ship and set its starting position. Creates settings attribute for Ship to be used in update().

    def update(self): Updates the ship's position based on the movement flags.

    def blitme(self): Draws the ship at its current location on the screen specified by self.rect.

    def center_ship(self): Center the ship on the screen.



