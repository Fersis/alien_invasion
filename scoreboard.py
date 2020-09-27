from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    """
    demonstrate score
    """

    def __init__(self, settings, screen, stats):
        """
        initialize attribute corresponding to scores
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """
        render the score into an image
        """
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.settings.scoreboard_text_font.render(
            'Score: ' + score_str, True, self.settings.scoreboard_text_color)

        # place the score in the right top of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        """
        render the history highest score
        """
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.settings.high_score_text_font.render(
            'Highest score: ' + high_score_str, True, self.settings.scoreboard_text_color)

        # place the score in the middle top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop
        self.high_score_rect.y += 10

    def prep_level(self):
        """
        render player level
        """
        self.level_image = self.settings.scoreboard_text_font.render(
            'Level: ' + str(self.stats.level), True, self.settings.level_color)

        # place level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.midtop = self.score_rect.midbottom
        self.level_rect.y += 20

    def prep_ships(self):
        """
        create remaining ships group
        """
        self.ships = Group()
        # create as many ships as reaminig ships
        for remaining_ship in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            # place ships in order
            ship.rect.x = 10 + (remaining_ship * ship.rect.width + 5)
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """
        show score in the screen
        show highest score in the screen
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
