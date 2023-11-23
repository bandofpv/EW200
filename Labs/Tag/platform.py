# TODO: Finish MovingPlatform class description AND change the picture too?

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
        self.xvelocity = 0

    def draw(self, screen):
        """Draws the Platform Sprite on the `screen` Surface.

        Args:
            screen (pygame.Surface): pygame.Surface of the screen to draw the Platform Sprite on.
        """
        screen.blit(self.image, self.rect)


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, size, side, speed, move_time, direction):
        super().__init__()
        self.image = pygame.image.load(f'assets/images/tile_half_{side}.png')
        self.image = pygame.transform.smoothscale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.xvelocity = self.speed
        self.move_time = move_time
        self.time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.direction = direction

    def move_right(self):
        self.xvelocity = self.speed
        self.rect.move_ip(self.speed, 0)

    def move_left(self):
        self.xvelocity = -self.speed
        self.rect.move_ip(-self.speed, 0)

    def update(self):
        self.time = pygame.time.get_ticks()
        if self.direction == 'right':
            self.move_right()
            if self.time - self.start_time > self.move_time:
                self.direction = 'left'
                self.start_time = self.time
        else:
            self.move_left()
            if self.time - self.start_time > self.move_time:
                self.direction = 'right'
                self.start_time = self.time


class Plat(pygame.sprite.Sprite):
    def __init__(self, x, y, size, length, speed, move_time, direction, screen):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 0, 0)
        self.size = size
        self.length = length
        self.speed = speed
        self.move_time = move_time
        self.direction = direction
        self.screen = screen
        self.group = pygame.sprite.Group()

        platform_width = size[0]
        for i in range(x + platform_width, x + length - platform_width, platform_width):
            self.group.add(Platform(i, y, size, 'center'))
        self.group.add(Platform(x, y, size, 'left'))
        self.group.add(Platform(x + length - platform_width, y, size, 'right'))

    def update(self):
        pass

    def draw(self):
        for platform in self.group:
            self.screen.blit(platform, self.rect)

