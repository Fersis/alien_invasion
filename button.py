import pygame


class Button():
    """game begin button"""

    def __init__(self, settings, screen, msg):
        """
        initialization function
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # button size and it's location
        self.rect = pygame.Rect(
            0, 0, settings.button_width, settings.button_height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg, settings)

    def prep_msg(self, msg, settings):
        """
        render the text into image and place it in the center of buttom
        """
        self.msg_image = settings.button_text_font.render(
            msg, True, settings.button_text_color, settings.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, settings):
        """
        draw the button and text
        """
        self.screen.fill(settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

