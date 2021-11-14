class GameStats():
    '''Monitoring statistic data in the game'''

    def __init__(self, ai_game):
        '''initializing statistic data'''
        self.settings = ai_game.settings
        self.reset_stats()

        # best score should not be erased ever
        self.high_score = 0

        # starting the game in active state
        self.game_active = False

    def reset_stats(self):
        '''initializing statistic data, that may change during the game'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
