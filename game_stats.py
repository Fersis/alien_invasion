


class GameStats():
    """ trace game infomation """

    def __init__(self, settings):
        """initialize infomation"""
        self.settings = settings
        self.reset_stats()
        self.game_active = False

        # read the highest score stored in the score.dat file
        try:
            with open('score.dat') as fin:
                self.high_score = int(fin.read())
        except FileNotFoundError:
            self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.settings.initialize_dynamic_settings()
        self.score = 0
        self.level = 1
