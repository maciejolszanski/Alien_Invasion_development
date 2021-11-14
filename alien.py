import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''single alien, member of the alien fleet'''

    def __init__(self,ai_game):
        '''Initialize the alien and his initial position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # importing the alien image and setting his rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # placing the alien near the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # flot x position of the alien
        self.x = float(self.rect.x)
    
    def update(self):
        '''moving alien right'''
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
    
    def check_edges(self):
        '''Returns True if any alien touches the edge of the screen'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False
