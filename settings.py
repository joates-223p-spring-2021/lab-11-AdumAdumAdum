import random as r

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_gameover = (100, 0, 0)
        self.init_color = (30, 0, 60)

        # Ship settings
        self.ship_speed = 0
        self.ship_speed_max = 1
        self.ship_accel = 0.005
        self.ship_size = 64

        # Bullet Settings
        self.bullet_true_random = True
        self.randomize_weapon(self.bullet_true_random)

        #Alien Settings
        #self.alien_speed = 0.2 #Default 0.2 # DYNAMIC
        self.fleet_drop_speed = 10 #Default 10
        #self.fleet_direction = 1 # pos = right, neg = left # DYNAMIC
        self.alien_points = 50
        self.alien_score_scale = 1.5

        #Round Progression Settings
        self.speedup_scale = 1.2
        
        self.initialize_dynamic_settings()

        #Stats Settings
        self.stats_max_lives = 3

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""

        self.alien_speed = 0.2
        self.fleet_direction = 1
        self.alien_points = 50
        self.bg_color = (30, 0, 60)

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed_max *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.fleet_direction = 1
        self.randomize_weapon(self.bullet_true_random)
        self.bg_color = ((r.randint(0,60),
                        r.randint(0,60),
                        r.randint(0,60)))
        self.alien_points = int(self.alien_points * self.alien_score_scale)

    def randomize_weapon(self, true_random):
        """Give the player a random weapon"""
        if true_random:
                self.bullet_speed = r.uniform(0.5, 3)
                self.bullet_width = r.triangular(4, 64, 8) 
                self.bullet_height = r.triangular(4, 64, 16) 
                self.bullet_color = (r.randint(0,255),
                                    r.randint(0,255),
                                    r.randint(0,255)) 
                self.bullet_max = r.triangular(1, 10, 3)
                self.bullet_pierce = r.choice((True, False)) 
                self.bullet_gravity = r.choice((True, False))
                self.bullet_weight = 0.0048
                self.bullet_lob_speed = 2.5 
        else:
            weapon = r.randint(1,3)
            if weapon == 1: #STANDARD GUN
                self.bullet_speed = 1.5 
                self.bullet_width = 8 
                self.bullet_height = 8 
                self.bullet_color = (245,54,54) 
                self.bullet_max = 5 
                self.bullet_pierce = False 
                self.bullet_gravity = False
                self.bullet_weight = 0
                self.bullet_lob_speed = 0 
    
            elif weapon == 2: #SLOW PIERCE LASER
                self.bullet_speed = 1
                self.bullet_width = 4 
                self.bullet_height = 128 
                self.bullet_color = (227,59,146) 
                self.bullet_max = 3 
                self.bullet_pierce = True 
                self.bullet_gravity = False
                self.bullet_weight = 0
                self.bullet_lob_speed = 0 

            elif weapon == 3: #HEAVY LOBSHOT
                self.bullet_width = 32 
                self.bullet_height = 32 
                self.bullet_color = (242, 138, 34) 
                self.bullet_max = 2 
                self.bullet_pierce = True 
                self.bullet_gravity = True 
                self.bullet_weight = 0.0048 
                self.bullet_lob_speed = 2.5 


