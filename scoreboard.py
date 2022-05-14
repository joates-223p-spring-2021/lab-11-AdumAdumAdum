import pygame.font 
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to represent scoring information"""

    def __init__(self, ai_game):
        """Intialize scorekeeping attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ai_game = ai_game

        # Font settings for scoring info
        self.text_color = (255, 210, 0)
        self.font = pygame.font.SysFont('consolas', 48)

        # Get high score from save file
        with open('high_score.txt', 'r') as f:
            self.stats.high_score = int(f.read())
            f.close()

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        str_score = str("{}".format(rounded_score))
        self.score_image = self.font.render(str_score, True, self.text_color, self.settings.bg_color)

        # Display at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 10

    def prep_high_score(self):
        """Turn the high score into a renderd image"""
        rounded_high = round(self.stats.high_score, -1)
        str_high = str("{}".format(rounded_high))
        self.high_image = self.font.render(str_high, True, self.text_color, self.settings.bg_color)

        # Display at the top right of the screen
        self.high_rect = self.high_image.get_rect()
        self.high_rect.right = self.screen_rect.centerx
        self.high_rect.top = self.high_rect.top

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        
        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.lives):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width*1.2
            ship.rect.y = 10
            self.ships.add(ship)
    
    def show_score(self):
        """Draw score and level to screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_image, self.high_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        self.prep_high_score()
        self.prep_score()

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score


