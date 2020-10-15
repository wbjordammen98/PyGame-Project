class Settings:
    # Class that stores all settings for Alien Invasion.

    def __init__(self):
        # Initializes the game's static settings.

        # Screen settings:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # Ship settings:
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings:
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings:
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left. 
        self.fleet_direction = 1

        # Controls how quickly the game speeds up.
        self.speedup_scale = 1.1

        # Shows how quickly the alien points increase.
        self.score_scale = 1.5
        # Initializes the values for the attributes that need to change throughout the game. 
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Initializes settings that change throughout the game. 

        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # Fleet direction of 1 represents right; -1 represents left. 
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        # Increases speed settings and alien point values.

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        # Increases the game's speed and the point value of each hit. 
        self.alien_points = int(self.alien_points * self.score_scale)
        