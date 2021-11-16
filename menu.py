import pygame

from pygame.sprite import Group
from button import Button


class Menu():

    def __init__(self, ai_game):
        '''initialize attributes of the menu'''
        self.ai_game = ai_game
        self.screen = self.ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.buttons = pygame.sprite.Group()
        self.buttonlist = ai_game.settings.buttonlist

        self.clicked_but = None

    def draw_menu(self):
        '''drawing buttons of the menu'''
        
        # creating button which I use to calculate buttons positions
        button_for_calc = Button(self.ai_game, 'CALCULATIONS ONLY')
        distance_between_buttons = 30
        available_space_y = (len(self.buttonlist) * button_for_calc.height
            + (len(self.buttonlist) - 1) * distance_between_buttons)
        
        iterations = 0

        # create each button from the list
        for button_name in self.buttonlist:
           
            # calculate button y position
            button_centery = (self.screen_rect.centery -
                available_space_y/2 + iterations*(button_for_calc.height +
                distance_between_buttons))

            created_button = Button(self.ai_game, button_name, button_centery)

            # add created button to the button sprites list and draw him
            self.buttons.add(created_button)
            created_button.draw_button()

            iterations += 1

    def is_any_button_clicked(self, mouse_pos):
        '''checking if any button is clicked'''
        for button in self.buttons.sprites():
            button_clicked = button.rect.collidepoint(mouse_pos)

            #check what is the message of the clicked button
            if button_clicked:
                self.clicked_but = button.msg
                break
            else:
                self.clicked_but = None
            
        return self.clicked_but
                
