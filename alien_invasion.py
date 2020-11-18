import pygame
from game_functions import check_events, update_aliens, update_bullets, update_screen
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from galaxy import Galaxy
from ship import Ship
from button import Button
from scoreboard import Scoreboard
from sound import Sound


def run_game():
    """ initialize game """

    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # create a gamestats instance
    stats = GameStats(settings)

    # create game background
    galaxy = Galaxy(screen)

    # create a ship
    ship = Ship(settings, screen)

    # create bullets group
    bullets = Group()

    # create aliens group
    aliens = Group()

    # create the play button
    play_button = Button(settings, screen, 'Play')

    # create a score board
    scoreboard = Scoreboard(settings, screen, stats)

    # create sound buffer
    sound = Sound()

    # begin game main while
    while True:
        check_events(settings, screen, stats, ship,
                     bullets, aliens, play_button, scoreboard, sound)

        if stats.game_active:
            ship.update_location()
            update_bullets(settings, screen, stats, ship,
                           bullets, aliens, scoreboard, sound)
            update_aliens(settings, screen, stats, ship,
                          bullets, aliens, scoreboard, sound)

        update_screen(settings, screen, stats, galaxy, ship,
                      bullets, aliens, play_button, scoreboard)


run_game()
