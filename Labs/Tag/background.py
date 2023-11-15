import pygame
from pygame import *
import pygame.freetype
from sprites import *


def build_border(screen, size, platform_group):
    """Builds border surrounding the screens perimeter.

    This function creates multiple Platform Sprites around the screen's perimeter. The top, left, and right edges of
    the screen are placed right outside the visible portion of the screen. The bottom edge is visible along the bottom
    side of the screen.

    Args:
        screen (pygame.Surface): Surface of display screen.
        size (tuple[int, int]): Tuple(width, height) of Platform tile size to surround the screen's perimeter.
        platform_group (pygame.sprite.Group): Sprite Group for Platform Sprites.

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


def build_platform(x, y, size, length, platform_group, screen):
    """Builds Platform of given `length`.

    This function creates multiple Platform Sprites to take up a given horizontal length and adds it to the given Sprite
    Group. The top left corner of the Platform is located on the given `x`, `y` location.

    Args:
        x (int): x-axis location to place Platform.
        y (int): y-axis location to place Platform.
        size (tuple[int, int]): Tuple[width, height] of Platform tile size.
        length (int): Length of Platform.
        platform_group (pygame.sprite.Group): Sprite Group for Platform Sprites.
        screen (pygame.Surface): Surface of display screen.

    """
    platform_width = size[0]
    screen_width = screen.get_width()
    if x + length > screen_width:
        length -= ((x + length) - screen_width)
    for i in range(x+platform_width, x+length-platform_width, platform_width):
        platform_group.add(Platform(i, y, size, 'center'))
    platform_group.add(Platform(x, y, size, 'left'))
    platform_group.add(Platform(x+length-platform_width, y, size, 'right'))


def start_screen(screen, game_events, font_size):
    """Displays Start Screen.

    Displays a 'Play' button at center of display screen.

    Args:
        screen (pygame.Surface): Surface of display screen.
        game_events (list): Pygame event list.
        font_size (int): Size of font.

    Returns:
        bool: True if clicked on 'Play' button, False if otherwise.

    """
    if button_collide(screen.get_rect().center, 'Play', font_size, screen, 1.1):
        for e in game_events:
            if e.type == pygame.MOUSEBUTTONDOWN:  # If mouse click, return True
                return True


def play_again(screen, game_events, it, font_size):
    """Displays Play Again Screen.

    Displays 'Play Again' button and announces winner.

    Args:
        screen (pygame.Surface): Surface of display screen.
        game_events (list): Pygame event list.
        it (tuple[bool, bool]): Tuple(green, blue) of green and blue Player `it` attributes. True if it, False if not it.
        font_size (int): Size of int.

    Returns:
        bool: True if clicked on 'Play Again' button, False if otherwise.

    """
    # If mouse cursor collides with 'Play Again' button located at the center of the screen
    if button_collide(screen.get_rect().center, 'Play Again', font_size, screen, 1.05):
        for e in game_events:
            if e.type == pygame.MOUSEBUTTONDOWN:  # If mouse click, return True
                return True
    winner_font = pygame.font.Font('assets/fonts/rush.otf', int(font_size * 0.7))
    green, blue = it
    if green:  # If green is it, display 'Blue Wins'
        winner_text = winner_font.render('Blue Wins', 1, 'blue')
    else:  # If blue is it, display 'Green Wins'
        winner_text = winner_font.render('Green Wins', 1, 'green')
    winner_rect = winner_text.get_rect()
    # Display winner_text at center top of display screen
    winner_rect.center = (screen.get_rect().centerx, screen.get_rect().centery - 130)
    screen.blit(winner_text, winner_rect)


def text_collision_rect(center, title, font_size):
    button_font = pygame.font.Font('assets/fonts/rush.otf', font_size)
    button_text = button_font.render(title, 1, (255, 255, 255))
    button_rect = button_text.get_rect()
    glyph_rect = pygame.mask.from_surface(button_text).get_bounding_rects()[0]
    offset = glyph_rect.top - button_rect.top
    collision_rect = pygame.Rect(0, 0, button_rect.width, glyph_rect.height)
    collision_rect.center = center
    return collision_rect, offset


def button_collide(center, title, font_size, screen, scale=1.0, swap_color='white'):
    button_font = pygame.font.Font('assets/fonts/rush.otf', font_size)
    button_text = button_font.render(title, 1, 'white')
    button_rect = button_text.get_rect()
    collision_rect, offset = text_collision_rect(center, title, font_size)
    if collision_rect.collidepoint(pygame.mouse.get_pos()):
        button_font = pygame.font.Font('assets/fonts/rush.otf', int(font_size * scale))
        button_text = button_font.render(title, 1, swap_color)
        button_rect = button_text.get_rect()
        collision_rect, offset = text_collision_rect(center, title, int(font_size * scale))
        button_rect.midtop = (collision_rect.centerx, collision_rect.top)
        button_rect.top -= offset
        screen.blit(button_text, button_rect)
        return True
    button_rect.midtop = (collision_rect.centerx, collision_rect.top)
    button_rect.top -= offset
    screen.blit(button_text, button_rect)


class Button:
    def __init__(self, center, title, font_size, font_color, screen):
        self.center = center
        self.title = title
        self.font_size = font_size
        self.font_color = font_color
        self.screen = screen
        self.font = pygame.font.Font('assets/fonts/rush.otf', self.font_size)
        self.text = self.font.render(title, 1, self.font_color)
        self.rect = self.text.get_rect(center=center)
        self.collision_rect = pygame.Rect(0, 0, 0, 0)

    def calc(self):
        calc_rect = pygame.Rect((0, 0), (self.rect.width, self.rect.height))
        glyph_rect = pygame.mask.from_surface(self.text).get_bounding_rects()[0]
        offset = glyph_rect.top - calc_rect.top
        self.collision_rect = pygame.Rect(0, 0, self.rect.width, glyph_rect.height)
        self.collision_rect.center = self.center
        self.rect.midtop = (self.collision_rect.centerx, self.collision_rect.top)
        self.rect.top -= offset

    def click(self, game_events, scale, font_color='white'):
        if self.collision_rect.collidepoint(pygame.mouse.get_pos()):
            self.font = pygame.font.Font('assets/fonts/rush.otf', int(self.font_size * scale))
            self.text = self.font.render(self.title, 1, font_color)
            self.rect = self.text.get_rect(center=self.center)
            self.calc()
            for e in game_events:
                if e.type == pygame.MOUSEBUTTONDOWN:  # If mouse click, return True
                    return True
        else:
            self.font = pygame.font.Font('assets/fonts/rush.otf', self.font_size)
            self.text = self.font.render(self.title, 1, self.font_color)
            self.rect = self.text.get_rect(center=self.center)
            self.calc()
        self.screen.blit(self.text, self.rect)


def quit_button(screen, game_events, font_size):
    x, y = screen.get_rect().centerx, screen.get_rect().centery + 140
    if button_collide((x, y), 'Quit', font_size, screen, swap_color='Red'):
        for e in game_events:
            if e.type == pygame.MOUSEBUTTONDOWN:  # If mouse click, return True
                return True


def build_level(size, platform_group, screen):
    build_platform(600, 500, size, 300, platform_group, screen)
    build_platform(400, 400, size, 200, platform_group, screen)
    build_platform(200, 300, size, 200, platform_group, screen)
    build_platform(700, 200, size, 8000, platform_group, screen)


def display_mouse(visible, game_events):
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


class Timer:
    def __init__(self, game_time, screen):
        self.game_font = pygame.font.Font('assets/fonts/rush.otf', 120)
        self.text = self.game_font.render('Hi', 1, (255, 0, 0))
        self.rect = self.text.get_rect()
        self.rect.midtop = screen.get_rect().midtop
        self.time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.game_time = game_time * 1000
        self.screen = screen
        self.play = True

    def update(self):
        timer = (self.game_time + self.start_time) - self.time
        if timer > 0:
            self.time = pygame.time.get_ticks()
        else:
            self.time = self.game_time
            self.play = False
        self.text = self.game_font.render(str(int(timer/1000)), 1, (255, 0, 0))
        self.rect = self.text.get_rect()
        self.rect.midtop = self.screen.get_rect().midtop

    def draw(self):
        self.screen.blit(self.text, self.rect)
