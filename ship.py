import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen):
        """initialize ship and set it's initial position"""
        super().__init__()
        self.screen = screen
        self.settings = settings

        # load ship image
        self.image = pygame.image.load('images/ship.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # place ship in the middle bottom of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # use center instead of centerx because center can store decimal
        self.center = float(self.rect.centerx)

        # movement mark
        self.moving_right = False
        self.moving_left = False

    def update_location(self):
        if (self.moving_right == True) and (self.rect.centerx < self.screen_rect.right):
            self.center += self.settings.ship_speed_factor

        if (self.moving_left == True) and (self.rect.centerx > self.screen_rect.left):
            self.center -= self.settings.ship_speed_factor

        # transfer float center to int centerx
        self.rect.centerx = self.center

    def blitme(self):
        """draw ship in the specific place"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """place ship in the center of bottom"""
        self.center = self.screen_rect.centerx
