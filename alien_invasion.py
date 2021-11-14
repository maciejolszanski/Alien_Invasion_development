import sys, pygame
from time import sleep

from pygame import mouse

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion():
    '''General Class to manage resources and control the game'''

    def __init__(self):
        '''Initialize the game, create the resources of the game'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        
        #DECOMMENT TO PLAY IN FULLSCREEN MODE
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_height = self.screen.get_rect().width
        #self.settings.screen_width = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        # creating an object storing statistic data of the game
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_alien_fleet()

        self.play_button = Button(self, "GRA")
        self.sb = Scoreboard(self)

    def run_game(self):
        '''Start the main loop of the game'''
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        '''react to keyboard or mouse press'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        '''reacting to key press'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        '''reacting to key release'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False    

    def _check_play_button(self, mouse_pos):
        '''Starting the game after clicking on PLAY button'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Clearing stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()
            self.sb.prep_level()

            # Resetting speed settings
            self.settings.initialize_dynamic_settings()

            # deleting aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # reseting the fleet and ship position
            self._create_alien_fleet()
            self.ship.center_ship()

            # hiding mouse coursor during gameplay
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        '''creating new bullet and adding it to the group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_alien_fleet(self):
        '''Creating alien fleet'''
        # Creating alien to calculate the number of the aliens on the screen
        # it is not added to the self.aliens 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # calculate the number of aliens in the row
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #calculate the number of rows
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Creating the alien fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(row_number, alien_number)

    def _create_alien(self, row_number, alien_number):
        '''Creating an alien and placing him in the row'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''changing direction when alien meets the edge of the screen'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''moving the fleet down and changing it's direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        '''reacting to hitting ship by an alien '''

        self.stats.ships_left -= 1
        self.sb.prep_ships()

        # Player has another "life"
        if self.stats.ships_left > 0:
            # deleting aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # game starts once again
            self._create_alien_fleet()
            self.ship.center_ship()

            self._update_screen()
            sleep(0.5)
        # Player does not have another "life"
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        '''checking if any alien hits the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_bullets(self):
        '''update bullet position and delete those beyond the screen'''
        # update bullet position
        self.bullets.update()

        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        
        self._check_bullet_alien_collision()
        
    def _check_bullet_alien_collision(self):
        '''reacting to bullet and alien collision'''
        # checking if any bullet met alien, if so - delete alien and bullet
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # checking if there is no alien left (empty group returns False)
        if not self.aliens:
            # deleting exisiting bullet and creating a new fleet
            self.bullets.empty()
            self._create_alien_fleet()
            self.settings.increase_speed()  

            # increment level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        '''
        Checking if any alien touches the edge 
        and then updating position of each alien
        '''
        self._check_fleet_edges()
        self.aliens.update()

        # detecting alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # checking if any alien met the bottom of the screen
        self._check_aliens_bottom()

    def _update_screen(self):
        '''updating images on the screen and changing screens'''
        # refreshing the screen in each iteration of the main loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.sb.show_score()
        
        # display button only when the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        # display last modification of the screen
        pygame.display.flip()

        
if __name__ == '__main__':
    # creating object of the game and running the game
    ai = AlienInvasion()
    ai.run_game()