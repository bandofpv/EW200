# TODO: Change font from white to red for last 10 seconds of the game

import pygame


class Timer:
    def __init__(self, game_time, screen):
        """Creates instance of Timer class.

        Args:
            game_time (int): Length of game in seconds.
            screen (pygame.Surface): pygame.Surface of the `screen` to draw the remaining time left in game.
        """
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
        """Updates the remaining time left in game.

        """
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
        """Draws the remaining time left in game on the `screen` Surface

        """
        self.screen.blit(self.text, self.rect)
