import json

class GameStats():
    '''Monitoring statistic data in the game'''

    def __init__(self, ai_game):
        '''initializing statistic data'''
        self.settings = ai_game.settings
        self.reset_stats()

        # reading hish score from the file 
        # or setting it to 0 if the file does not exist
        self.high_score_path = 'data/high_score'
        try:
            with open(self.high_score_path, 'r') as f:
                self.high_score = json.load(f) 
        except:
            self.high_score = 0
        
        # starting the game in active state
        self.game_active = False

    def reset_stats(self):
        '''initializing statistic data, that may change during the game'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        # setting the flag to set new high score to False
        self.save_new_high_score_flag = False
