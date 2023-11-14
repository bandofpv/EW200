import pygame
from pygame import *
import pygame.freetype
from sprites import *


def build_border(screen, size, platform_group):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    platform_width = size[0]
    platform_height = size[1]
    for x in range(0, screen_width, platform_width):
        platform_group.add(Platform(x, -platform_height, size, 'center'))
        platform_group.add(Platform(x, screen_height-platform_height, size, 'center'))
    for y in range(0, screen_height, platform_height):
        platform_group.add(Platform(-platform_width, y, size, 'center'))
        platform_group.add(Platform(screen_width, y, size, 'center'))


def build_platform(x, y, size, length, platform_group, screen):
    platform_width = size[0]
    screen_width = screen.get_width()
    if x + length > screen_width:
        length -= ((x + length) - screen_width)
    for i in range(x+platform_width, x+length-platform_width, platform_width):
        platform_group.add(Platform(i, y, size, 'center'))
    platform_group.add(Platform(x, y, size, 'left'))
    platform_group.add(Platform(x+length-platform_width, y, size, 'right'))


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


def start_menu(screen, game_events, font_size):
    button_font = pygame.font.Font('assets/fonts/rush.otf', font_size)
    button_text = button_font.render('Play', 1, (255, 255, 255))
    if text_collide(button_text.get_rect(center=screen.get_rect().center), font_size):
        button_font = pygame.font.Font('assets/fonts/rush.otf', int(font_size*1.1))
        button_text = button_font.render('Play', 1, (255, 255, 255))
        for e in game_events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                return True
    button_rect = button_text.get_rect()
    button_rect.center = screen.get_rect().center
    screen.blit(button_text, button_rect)


def play_again(screen, game_events, it, font_size):
    button_font = pygame.font.Font('assets/fonts/rush.otf', font_size)
    button_text = button_font.render('Play Again', 1, (255, 255, 255))
    if text_collide(button_text.get_rect(center=screen.get_rect().center), font_size):
        button_font = pygame.font.Font('assets/fonts/rush.otf', int(font_size*1.05))
        button_text = button_font.render('Play Again', 1, (255, 255, 255))
        for e in game_events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                return True
    button_rect = button_text.get_rect()
    button_rect.center = screen.get_rect().center
    screen.blit(button_text, button_rect)
    winner_font = pygame.font.Font('assets/fonts/rush.otf', int(font_size * 0.7))
    green, blue = it
    if green:
        winner_text = winner_font.render('Blue Wins', 1, (0, 0, 255))
    else:
        winner_text = winner_font.render('Green Wins', 1, (0, 255, 0))
    winner_rect = winner_text.get_rect()
    winner_rect.center = (screen.get_width()/2, (screen.get_height()/2) - (font_size*0.7 + 70))
    screen.blit(winner_text, winner_rect)


def text_collide(text_rect, font_size):
    text_rect.height = font_size * 0.85
    if text_rect.collidepoint(pygame.mouse.get_pos()):
        return True


def quit_button(screen, game_events, font_size):
    quit_font = pygame.font.Font('assets/fonts/rush.otf', font_size)
    quit_text = quit_font.render('Quit', 1, (255, 255, 255))
    quit_rect = quit_text.get_rect()
    quit_rect.height = font_size
    quit_rect.center = (screen.get_width() / 2, (screen.get_height() / 2) + (60 + font_size))
    if text_collide(quit_rect, font_size):
        quit_text = quit_font.render('Quit', 1, (255, 0, 0))
        for e in game_events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                return True
    screen.blit(quit_text, quit_rect)


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
