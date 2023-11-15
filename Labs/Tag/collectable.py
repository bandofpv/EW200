import pygame


class Collectable(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f'assets/images/tile_exclamation.png')
        self.image = pygame.transform.smoothscale(self.image, [25, 25])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
