import pygame

from pygame.sprite import Sprite


class Button(Sprite):
    '''Defining a button'''

    def __init__(self, ai_game, msg, y_pos=400):
        '''initializing attributes of the button'''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # defining the button size and other properties
        self.width, self.height = 400, 90
        self.button_color = (0, 255, 0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 72)

        # creating buttons rect and centering it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = y_pos

        # preparing msg for the button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''Placing the message on the screen, and cetering it on the button'''
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''displaying empty button and then displaying the message'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
