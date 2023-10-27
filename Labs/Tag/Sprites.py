import pygame


# define a class called Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 3
        self.xvelocity = 0
        self.yvelocity = 0

    def update(self, platforms):
        key = pygame.key.get_pressed()
        ground = self.collision(0, 1, platforms)
        self.xvelocity = 0
        if key[pygame.K_LEFT]:
            self.xvelocity = -self.velocity
        if key[pygame.K_RIGHT]:
            self.xvelocity = self.velocity
        if key[pygame.K_UP] and ground:
            self.yvelocity = -20
        elif self.yvelocity < 9.81 and not ground:
            self.yvelocity += 1
        elif ground:
            self.yvelocity = 0
        self.move(self.xvelocity, self.yvelocity)

    def collision(self, x, y, platforms):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, platforms)
        self.rect.move_ip([-x, -y])
        return collide

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)