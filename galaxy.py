import pygame


class Galaxy():
    """
    background image class
    """
    def __init__(self, screen):
        self.image = pygame.image.load('images/galaxy.jpg').convert()
        self.screen = screen
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.center = self.screen_rect.center

    def draw(self):
        self.screen.blit(self.image, self.rect)
