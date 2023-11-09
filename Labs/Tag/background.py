import pygame
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
    def __init__(self, screen):
        self.game_font = pygame.font.Font('assets/fonts/rush.otf', 120)
        self.text = self.game_font.render('Hi', 1, (255, 0, 0))
        self.rect = self.text.get_rect()
        self.rect.midtop = screen.get_rect().midtop
        self.time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.screen = screen
        self.play = True

    def update(self):
        timer = (6000 + self.start_time) - self.time
        if timer > 0:
            self.time = pygame.time.get_ticks()
        else:
            self.time = 6000
            self.play = False
        self.text = self.game_font.render(str(int(timer/1000)), 1, (255, 0, 0))
        self.rect = self.text.get_rect()
        self.rect.midtop = self.screen.get_rect().midtop

    def draw(self):
        self.screen.blit(self.text, self.rect)


# class Menu:
#     def __init__(self, screen):
#         self.screen = screen
#         self.game_font = pygame.font.Font('assets/fonts/rush.otf', 60)
#         self.text = self.game_font.render('100 Play Again', 1, (255, 255, 0))
#         self.rect = self.text.get_rect()
#         self.rect.center = self.screen.get_rect().center
#
#     def update(self):
#         pass
#
#     def draw(self):
#         self.screen.blit(self.text, self.rect)


def play_again(screen, game_events):
    game_font = pygame.font.Font('assets/fonts/rush.otf', 60)
    text = game_font.render('100 Play Again', 1, (255, 255, 0))
    rect = text.get_rect()
    rect.center = screen.get_rect().center
    screen.blit(text, rect)
    for event in game_events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(pygame.mouse.get_pos()):
                return True

# def start_game(screen):
#