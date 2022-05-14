import pygame
from pygame.sprite import Sprite
from settings import Settings

class Ship(Sprite):
    """A class to manage the ship."""


    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get it's hitbox(?)
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Initialize the ship at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

        # ADUM - Speed variables
        self.hspd = self.settings.ship_speed
        self.accel = self.settings.ship_accel
        self.maxspd = self.settings.ship_speed_max

    def update(self):
        # Movement code w/ACCELERATION
        
        #If Colliding with wall:
        if self.rect.right > self.screen_rect.right:
            self.hspd = 0
            self.x = self.screen_rect.right - self.settings.ship_size

        elif self.rect.left < 0:
            self.hspd = 0
            self.x = 0

        # If right is pressed, accelerate right:
        if self.moving_right:

            if self.hspd < self.maxspd:
                self.hspd += self.accel
            self.x += self.hspd

        # If left is pressed, accelerate left:
        elif self.moving_left:

            if self.hspd > (-self.maxspd):
                self.hspd -= self.accel
            self.x += self.hspd

        # If nothing is pressed, slow down
        else:
            if self.hspd > 0: self.hspd -= self.accel
            if self.hspd < 0: self.hspd += self.accel
            if abs(self.hspd) < 0.1: self.hspd = 0
            self.x += self.hspd

        # Update rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x) 

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)




#IDEAS: 
#   1) Make ship have an acceleration and less friction
#   2) 