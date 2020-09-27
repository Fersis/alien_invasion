import pygame.font


class Settings():
    def __init__(self):
        """game setting"""

        ### static settigs ###
        # screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (255, 255, 255)

        # button settings
        self.button_width = 200
        self.button_height = 50
        self.button_color = (64, 224, 208)
        self.button_text_color = (255, 255, 255)
        self.button_text_font = pygame.font.SysFont(None, 48)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 185, 15)
        self.bullet_allowed = 20

        # alien settings
        self.fleet_drop_speed = 10

        # game scale settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # scoreboard settings
        self.scoreboard_text_color = (0, 255, 255)
        self.scoreboard_text_font = pygame.font.SysFont(
            'consolas', 32, bold=True)
        self.high_score_text_font = pygame.font.SysFont(
            'consolas', 24, bold=True
        )
        self.level_color = (255, 255, 0)

        ### dynamic settings ###
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        # fleet direction, 1 represents moving right and -1 represents moving left
        self.fleet_direction = 1

        # alien's score
        self.alien_point = 50

    def increase_speed(self):
        """
        increase dynamic parameter
        """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_point = int(self.alien_point * self.score_scale)
