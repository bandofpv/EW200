# TODO: Finish MovingPlatform class (add side to side capabilities)

import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, size, side):
        """Creates Platform Sprite.

        Note:
            Uses top left corner convention for tile position.

        Args:
            x (int): x-axis location of Platform Sprite.
            y (int): y-axis location of Platform Sprite.
            size (tuple[int, int]): Tuple[width, height] of Platform tile size.
            side (str): String ('center', 'left', or 'right') of Platform tile side.

        """
        super().__init__()
        self.image = pygame.image.load(f'assets/images/tile_{side}.png')
        self.image = pygame.transform.smoothscale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 0

    def draw(self, screen):
        """Draws the Platform Sprite on the `screen` Surface.

        Args:
            screen (pygame.Surface): pygame.Surface of the screen to draw the Platform Sprite on.
        """
        screen.blit(self.image, self.rect)


class MovingPlatform(Platform):
    def __init__(self, x, y, size, side, speed):
        super().__init__(x, y, size, side)
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed, 0)
