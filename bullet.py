import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen

        # create bullet and put it on right place
        self.rect = pygame.Rect(
            0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store bullet place with float number
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self, bullets):
        self.y -= self.speed_factor
        self.rect.y = self.y
        if self.rect.y <= 0:
            bullets.remove(self)

    def draw_bullet(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
