import pygame.font
import json

from pygame.sprite import Group
from os import path, mkdir

from ship import Ship

class Scoreboard():
    '''Displaying score and other gampeplay info'''

    def __init__(self,ai_game):
        '''Initializae score attribtes'''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # setting the font
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        # preparing the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''Converting score to image'''
        rounded_score = round(self.stats.score, -1)
        score_str = "SCORE: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)
        
        # Display the score in top right corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = 20
        self.score_rect.right = self.screen_rect.right - 20

    def prep_high_score(self):
        '''Convert best score to image'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = "BEST: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)
        
        # Display the score in top right corner
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = self.score_rect.top 
        self.high_score_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        '''Convert level number to image'''
        level_str = 'LVL: ' + str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)
        
        # Level displayed under actual score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.score_rect.right

    def prep_ships(self):
        '''Display number of left ships - lives'''
        self.ships = Group()
        for ship_number in range (self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        '''checking if the new score is the highest'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            # sets the flag to save new high score to .json file 
            # at the end of the game
            self.stats.save_new_high_score_flag = True

    def save_new_high_score_to_file(self):
        '''Writing the new high score to .json'''
        # getting the directory name from the path
        path_list = self.stats.high_score_path.split('/')
        directory_name = path_list[0]

        # checking if such directory exists and creating it if it does not
        if not path.exists(directory_name):
            mkdir(directory_name)
        # writing high score to file
        with open(self.stats.high_score_path, 'w') as f:
                json.dump(self.stats.high_score, f)


    def show_score(self):
        '''Display the score on the screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)