# TODO: finish function descriptions

import pygame
import pygame.freetype
from platform import Platform, MovingPlatform
from collectible import Collectible
from random import randrange, triangular, normalvariate, choice


def build_border(screen, size, platform_group):
    """Builds border surrounding the screens perimeter.

    This function creates multiple Platform Sprites around the screen's perimeter. The top, left, and right edges of
    the screen are placed right outside the visible portion of the screen. The bottom edge is visible along the bottom
    side of the screen.

    Args:
        screen (pygame.Surface): pygame.Surface of game screen.
        size (tuple[int, int]): Tuple(width, height) of Platform tile size to surround the screen's perimeter.
        platform_group (pygame.sprite.Group): pygame.sprite.Group for Platform Sprites.

    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    platform_width = size[0]
    platform_height = size[1]
    for x in range(0, screen_width, platform_width):  # loop along width of screen
        platform_group.add(Platform(x, -platform_height, size, 'center'))  # top edge
        platform_group.add(Platform(x, screen_height-platform_height, size, 'center')) # bottom edge
    for y in range(0, screen_height, platform_height):  # loop along height of screen
        platform_group.add(Platform(-platform_width, y, size, 'center'))  # left edge
        platform_group.add(Platform(screen_width, y, size, 'center'))  # right edge


def build_platform(x, y, size, length, platform_group):
    """Builds Platform of given `length`.

    This function creates multiple Platform Sprites to take up a given horizontal length and adds it to the given Sprite
    Group. The top left corner of the Platform is located on the given `x`, `y` location.

    Args:
        x (int): x-axis location to place Platform.
        y (int): y-axis location to place Platform.
        size (tuple[int, int]): Tuple[width, height] of Platform tile size.
        length (int): Length of Platform.
        platform_group (pygame.sprite.Group): pygame.sprite.Group for Platform Sprites.
        screen (pygame.Surface): pygame.Surface of game screen.
        speed (int): Speed of MovingPlatform. Defaults to 0 (static Platform).

    """
    platform_width = size[0]
    for i in range(x + platform_width, x + length - platform_width, platform_width):
        platform_group.add(Platform(i, y, size, 'center'))
    platform_group.add(Platform(x, y, size, 'left'))
    platform_group.add(Platform(x + length - platform_width, y, size, 'right'))


def mv_platform(x, y, size, length, platform_group, speed, move_time, direction):
    platform_width = size[0]
    for i in range(x + platform_width - 15, x + length - platform_width, platform_width - 15):
        platform_group.add(MovingPlatform(i, y, size, 'center', speed, move_time, direction))
    platform_group.add(MovingPlatform(x, y, size, 'left', speed, move_time, direction))
    platform_group.add(MovingPlatform(x + length - platform_width, y, size, 'right', speed, move_time, direction))


def calc_length(length, speed, move_time):
    moving_length = length + speed * 60 * (move_time / 1000)
    return int(moving_length)


def build_game(size, platform_group, screen):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    platform_width = size[0]
    platform_height = size[1]
    for y in range(screen_height - platform_height - 100, 0, -100):
        first_plat = True
        was_moving = False
        count = 0
        while 0 <= count < screen_width:
            spacing = randrange(50, 100, 5)
            speed = int(triangular(0, 3, 0))
            # moving_time = 1700
            moving_time = randrange(700, 1700, 50)
            direction = choice(['right', 'left'])
            if round(triangular(0, 1, 0.75)) and first_plat:
                length = round(normalvariate(200, 100))
                length = 50 if length < 50 else 400 if length > 400 else length
                build_platform(0 - platform_width, y, size, length, platform_group)
                count += length - platform_width
            else:
                if speed and not was_moving:
                    length = round(normalvariate(100, 20))
                    length = 50 if length < 50 else 150 if length > 150 else length
                    moving_length = calc_length(length, speed, moving_time // speed)
                    if count + moving_length > screen_width:
                        build_platform(count + spacing, y, size, length, platform_group)
                        count += spacing + length
                        continue
                    spacing = 10
                    was_moving = True
                    if direction == 'right':
                        mv_platform(count + spacing, y, size, length, platform_group, speed, moving_time // speed,
                                    direction)
                    else:
                        mv_platform(count + spacing + moving_length - length, y, size, length, platform_group, speed,
                                    moving_time // speed, direction)
                    length = moving_length
                else:
                    if was_moving:
                        spacing = 10
                        was_moving = False
                    length = round(normalvariate(200, 100))
                    length = 50 if length < 50 else 400 if length > 400 else length
                    build_platform(count + spacing, y, size, length, platform_group)
                count += spacing + length
                print(direction)
            first_plat = False


def display_winner(screen, player1, player2, font_size):
    """Displays winner of the game.

    Displays the Player who is not `it` as the winner at top of screen and in the `color` of the Player.

    Args:
        screen (pygame.Surface): pygame.Surface of game screen.
        player1 (Player): Instance of first player.
        player2 (Player): Instance of second player.
        font_size (int): Size of font.

    """
    winner_font = pygame.font.Font('assets/fonts/rush.otf', int(font_size * 0.7))
    if player1.it:  # If player1 is it, player2 wins
        winner_text = winner_font.render(f'{player2.color.title()} Wins', 1, f'{player2.color}')
    else:  # If player2 is it, player1 wins
        winner_text = winner_font.render(f'{player1.color.title()} Wins', 1, f'{player1.color}')
    winner_rect = winner_text.get_rect()
    # Display winner_text at center top of display screen
    winner_rect.center = (screen.get_rect().centerx, screen.get_rect().centery - 130)
    screen.blit(winner_text, winner_rect)


def display_cursor(visible, game_events):
    """Determines whether to display cursor based on given `visible` and `game_events` arguments.

    Used to display or not display cursor during gameplay. See `main.py` for example usage.

    Args:
        visible (bool): True if mouse is visible, False if otherwise.
        game_events (list[pygame.Event]): List[pygame.event] of pygame events.

    Returns:
        bool: True if `visible` is True. True if `visible` is False, but escape button clicked or detected mouse motion.
            False if `visible` is True and mouse button is clicked.

    """
    for e in game_events:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE and not visible:
                return True
        elif e.type == pygame.MOUSEMOTION and not visible:
            return True
        elif e.type == pygame.MOUSEBUTTONDOWN and visible:
            return False
    if visible:
        return True
    return False
