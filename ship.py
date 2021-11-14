import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Star ship'''

    def __init__(self, ai_game):
        '''inititalize the ship and set its initial position'''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Importing the ship image and getting his rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Each new ship appers in the middle bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Ship position in float number
        self.x = float(self.rect.x)

        # Attributes of moving the ship
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Updating ship's position regarding on the moving attributes'''
        # updating ships float x position - not his rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        # updating rect.x based on float self.x
        self.rect.x = self.x

    def blitme(self):
        '''Showing the ship with actual position'''
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        '''Centering the ship on the bottom of the screen'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)