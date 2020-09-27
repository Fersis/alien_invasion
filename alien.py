import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Alien class"""

    def __init__(self, settings, screen):
        super().__init__()
        self.settings = settings
        self.screen = screen

        # load image
        self.image = pygame.image.load('images/alien_ship.png').convert_alpha()
        # get rectengular
        self.rect = self.image.get_rect()

        # set it's initial location in left top
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien's accurate location
        self.x = self.rect.x
        self.y = self.rect.y

    def blitme(self):
        """show alien"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        # moving alien right or left
        self.x += self.settings.alien_speed_factor*self.settings.fleet_direction
        self.rect.x = self.x

    def check_edge(self):
        """if alien reach the edge, return true"""
        screen_rect = self.screen.get_rect()
        # reach right edge
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True