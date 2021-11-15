class Settings():
    '''Storing every setiing of the game'''

    def __init__(self):

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        
        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (232, 205, 69)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # Content of the menu settings
        self.buttonlist = ["PLAY", "HOW TO PLAY", "SETTINGS", "INFO"]

        # Easy change of the game speed
        self.speedup_scale = 1.1
        # Eaasy score change
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize speed settings'''
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1.0

        # direction 1 - right, -1 - left
        self.fleet_direction = 1

        # Score
        self.alien_points = 50

    def increase_speed(self):
        '''Changing the speed settings'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)