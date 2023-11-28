# TODO: Randomize location of collectable and set it on a timer to kill itself

import pygame


class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """Creates Collectible Sprite.

        Args:
            x (int): x-axis location of Collectible Sprite.
            y (int): y-axis location of Platform Sprite.
        """
        super().__init__()
        self.image = pygame.image.load(f'assets/images/tile_exclamation.png')
        self.image = pygame.transform.smoothscale(self.image, [25, 25])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.start_time = pygame.time.get_ticks()
        self.time = pygame.time.get_ticks()

    def update(self):
        pass

    def draw(self, screen):
        """Draws the Collectible Sprite on the `screen` Surface.

        Args:
            screen (pygame.Surface): pygame.Surface of the screen to draw the Collectible Sprite on.
        """
        screen.blit(self.image, self.rect)
