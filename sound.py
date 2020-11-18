import pygame.mixer


class Sound():
    """
    sound effect
    """

    def __init__(self):
        self.sd_bg = pygame.mixer.Sound('sound/background.wav')
        self.sd_alien_hit = pygame.mixer.Sound('sound/explosion.mp3')

    def pl_bg(self):
        pygame.mixer.Sound.play(self.sd_bg, loops=-1)

    def pl_alien_hit(self):
        pygame.mixer.Sound.play(self.sd_alien_hit)

    def stop_all_sound(self):
        pygame.mixer.stop()