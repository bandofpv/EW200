import pygame


# define a class called Player
class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.image.fill((0,255,0))
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 1
    def update(self):
        self.rect.y += self.velocity
    def draw(self, screen):
        screen.blit(self.image, self.rect)
