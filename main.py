import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Manage game assets and behavior"""
    
####################
# INITIALIZE CLASS #
####################

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.play_button = Button(self, "Protect the Galaxy!")

        self._create_fleet()

        # Set the background color
        self.bg_color = (self.settings.init_color)

######################
# CHECK KEYS / MOUSE #
######################

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_KP6 or event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            f = open('high_score.txt', 'w')
            f.write(str(self.stats.high_score))
            f.close()
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
        else: pass

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        else: pass

    def _check_play_button(self, mouse_pos):
        #Start a new game when the player clicks play
        if self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _start_game(self):
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        #Hide Mouse cursor
        pygame.mouse.set_visible(False)

        #Get rid of any remaining aliens or bullets
        self.aliens.empty()
        self.bullets.empty()

        #Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

##################
# BULLET METHODS #
##################

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_max and self.stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Update bullet position
        self.bullets.update()
        
        # Delete old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_height: #ADUM ADDITION, REMOVE BULLETS THAT HIT THE BOTTM
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

#################
# ALIEN METHODS #
#################

    def _create_alien(self, alien_num, row_num):
        """Create an alien and place it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_num)
        alien.rect.x = alien.x
        alien.rect.y =  alien_height + (2 * alien.rect.height * row_num)
        self.aliens.add(alien)
        
    
    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        num_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        num_rows = available_space_y // (2 * alien_height)

        #Create full fleet of aliens
        for row_num in range(num_rows):
            for alien_num in range(num_aliens_x):
                self._create_alien(alien_num,row_num)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached and edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self._check_alien_ship_collisions()
        self._check_aliens_bottom()
        self.aliens.update()

#####################
# COLLISION METHODS #
#####################

    def _check_bullet_alien_collisions(self):
        #Check for any bullets that have collided with aliens, if so kill alien and bullet
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, not self.settings.bullet_pierce, True)
        
        if collisions: 
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
    

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.bg_color = self.settings.bg_color

            self.stats.level += 1
            self.sb.prep_level()

    def _check_alien_ship_collisions(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _screen_flash(self):
        pass
        #if.pygame.sprite


########################
# SHIP / STATS METHODS #
########################
    
    def _ship_hit(self):

        if self.stats.lives > 1:
            self.stats.lives -= 1
            self.sb.prep_ships()
            sleep(1)
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            #self.bg_color = self.bg_color + (20,0,0) #Attempt to add a background. Doesn't work
            #self.screen.fill(self.bg_color)
        
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


################
# GAME METHODS #
################

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)
        self.sb.show_score()

        #Draw button if the game isn't active
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

###################
# MAIN GAME LOGIC #
###################

if __name__ == "__main__":
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
            

# IDEAS: 
# 1) slippery ship. Movement speed is quadratic, not linear :)
# 2) Bullet that passes through enemies as an upgrade
# 3) Make background flash white or red when you kill an enemy
# 4) Bullet that has an arc, or is subject to gravity/lob :)
# 5) Make multiple levels that change the background color and speed up enemies / change weapon
# 6) Make a bullet either a laser that pierces enemies or a projectile that lobs, maybe a way to switch between the two
# 7) Make it so lob bullets kill you ship too
# 7b) Make it so you have to catch the lob bullet to use it again? standing still would be boring, only do this if the lob has an arc
# 8) Random mode that makes it so you get a random speed, a random weapon, and a random background color (random ship/alien/bullet size)?
                    