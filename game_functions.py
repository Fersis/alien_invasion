import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


# check event function
def check_events(settings, screen, stats, ship,
                 bullets, aliens, play_button, scoreboard, sound):
    # monitor keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # before exit the game, write the highest score into score.dat file
            with open('score.dat', 'w') as fout:
                fout.write(str(stats.high_score))
            # exit game
            sys.exit()

        # control ship direction
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, settings, screen,
                                stats, ship, bullets, aliens, scoreboard, sound)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, ship,
                              bullets, aliens, play_button, mouse_x, mouse_y, scoreboard, sound)


def check_keydown_event(event, settings, screen, stats,
                        ship, bullets, aliens, scoreboard, sound):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_RETURN:
        if not stats.game_active:
            start_game(settings, screen, stats, ship,
                       bullets, aliens, scoreboard, sound)


def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(settings, screen, ship, bullets):
    # check whether bullets touch it's limit
    if len(bullets) < settings.bullet_allowed:
        # create a bullet and add it to group
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def start_game(settings, screen, stats, ship,
               bullets, aliens, scoreboard, sound):
    """
    reset game status
    """
    stats.reset_stats()
    stats.game_active = True

    aliens.empty()
    bullets.empty()

    create_fleet(settings, screen, ship, aliens)
    ship.center_ship()

    # reprep the current score
    scoreboard.prep_score()
    # reprep the level to 1
    scoreboard.prep_level()
    # reprep remaining ships
    scoreboard.prep_ships()

    # begin playing background music
    sound.pl_bg()


def check_play_button(settings, screen, stats, ship,
                      bullets, aliens, play_button, mouse_x, mouse_y, scoreboard, sound):
    """
    check whether player click the play button
    if so, start game
    """
    if (play_button.rect.collidepoint(mouse_x, mouse_y) and
            not stats.game_active):
        start_game(settings, screen, stats, ship,
                   bullets, aliens, scoreboard, sound)


# update screen function
def update_screen(settings, screen, stats, galaxy, ship, bullets, aliens, play_button, scoreboard):
    # screen.fill(settings.bg_color)

    # draw background
    galaxy.draw()

    # if game is inactive, draw the play button
    if not stats.game_active:
        play_button.draw_button(settings)
    else:
        # draw ship
        ship.blitme()

        # draw bullets
        for bullet in bullets.sprites():
            bullet.draw_bullet(screen)

        # draw aliens
        aliens.draw(screen)

        # draw score board
        scoreboard.show_score()

    # show screen
    pygame.display.flip()


# update bullet function
def update_bullets(
        settings, screen, stats, ship, bullets, aliens, scoreboard, sound):
    """update bullet and check collision"""
    bullets.update(bullets)
    check_bullet_alien_collisions(
        settings, screen, stats, ship, bullets, aliens, scoreboard, sound)


def check_bullet_alien_collisions(settings, screen, stats, ship, bullets, aliens, scoreboard, sound):
    """
    add score, 
    check high score, 
    check remaining aliens
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # if collison happen, add score and check high score
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_point * len(aliens)
        scoreboard.prep_score()
        check_high_score(stats, scoreboard)
        # play the sound effect of alien being eliminated
        # it's very annoy although
        # sound.pl_alien_hit()


    check_aliens_fleet(settings, screen, stats, ship,
                       bullets, aliens, scoreboard)


def check_aliens_fleet(settings, screen, stats, ship, bullets, aliens, scoreboard):
    """
    check whether there are aliens remaining
    """
    # if no aliens, create new fleet and level up
    if len(aliens) == 0:
        # delete bullets, speed up game and create a new fleet
        bullets.empty()
        settings.increase_speed()
        create_fleet(settings, screen, ship, aliens)
        # level up
        stats.level += 1
        scoreboard.prep_level()


# create fleet function
def get_aliens_columns(settings, alien_width):
    """calculate how many aliens can one line contain"""
    # spacing between aliens is alien width
    available_space_x = settings.screen_width-2*alien_width
    aliens_columns = int(available_space_x/(2*alien_width))
    return aliens_columns


def get_aliens_rows(settings, alien_height, ship_height):
    """calculate how many rows of aliens can screen contain"""
    available_space_y = settings.screen_height-3*alien_height-ship_height
    aliens_rows = int(available_space_y/(2*alien_height))
    return aliens_rows


def create_alien(settings, screen, aliens, column, row):
    # create a alien and add it to group
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    alien.x = alien_width+2*alien_width*column
    alien.rect.x = alien.x

    alien.y = alien_height+2*alien_height*row
    alien.rect.y = alien.y

    aliens.add(alien)


def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    aliens_columns = get_aliens_columns(settings, alien.rect.width)
    aliens_rows = get_aliens_rows(
        settings, alien.rect.height, ship.rect.height)

    for aliens_column in range(aliens_columns):
        for aliens_row in range(aliens_rows):
            create_alien(settings, screen, aliens, aliens_column, aliens_row)


# update aliens function
def update_aliens(settings, screen, stats, ship, 
                  bullets, aliens, scoreboard, sound):
    check_fleet_edge(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, 
                 bullets, aliens, scoreboard, sound)
    check_aliens_bottom(settings, stats, screen, ship,
                        bullets, aliens, scoreboard, sound)


def check_fleet_edge(settings, aliens):
    """if any alien reach the edge, change fleet's direction"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    """"move all aliens down, change direction"""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def ship_hit(settings, stats, screen, ship, bullets, aliens, scoreboard, sound):
    """response to ship hit by alien"""
    if stats.ships_left > 1:
        # decrease ship left by 1
        stats.ships_left -= 1

        # prep ships group
        scoreboard.prep_ships()

        # empty aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and place new ship in the bottom middle of the screen
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(1)
    else:
        # close game and stop all music
        stats.game_active = False
        sound.stop_all_sound()


def check_aliens_bottom(settings, stats, screen, ship, bullets, aliens, scoreboard, sound):
    """check whether an alien reach bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # solve it like ship be hitted
            ship_hit(settings, stats, screen, ship,
                     bullets, aliens, scoreboard, sound)
            break


# check highest score function
def check_high_score(stats, scoreboard):
    """
    check whether there is a high score
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()
