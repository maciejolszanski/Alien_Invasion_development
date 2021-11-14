import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''bullets shot by the ship'''

    def __init__(self, ai_game):
        '''create a bullet in actual ship's position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # Creating a bullet rect in 0,0 point, and then changing his position
        self.rect = pygame.Rect(
            0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # bullet float position
        self.y = float(self.rect.y)

    def update(self):
        '''moving the bullet'''
        # New bullet's position
        self.y -= self.settings.bullet_speed
        # New bullet's rect position
        self.rect.y = self.y

    def draw_bullet(self):
        '''display the bullet'''
        pygame.draw.rect(self.screen, self.color, self.rect)
    