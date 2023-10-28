import pygame


# define a class called Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, keys):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 3
        self.xvelocity = 0
        self.yvelocity = 0
        self.right_key = keys[0]
        self.left_key = keys[1]
        self.up_key = keys[2]
        self.jumpvelocity = -15
        self.fallvelocity = 10

    def update(self, platforms):
        top_collide = self.touch(0, self.yvelocity, platforms)
        bottom_collide = self.touch(0, self.fallvelocity, platforms)
        right_collide = self.touch(self.velocity, 0, platforms)
        left_collide = self.touch(-self.velocity, 0, platforms)
        self.xvelocity = 0
        key = pygame.key.get_pressed()
        if key[self.left_key]:
            if left_collide and self.yvelocity == 0:
                self.rect.left = left_collide[0].rect.right
            elif left_collide:
                self.xvelocity = 0
            else:
                self.xvelocity = -self.velocity
        if key[self.right_key]:
            if right_collide and self.yvelocity == 0:
                self.rect.right = right_collide[0].rect.left
            elif right_collide:
                self.xvelocity = 0
            else:
                self.xvelocity = self.velocity
        if key[self.up_key] and self.yvelocity == 0 and bottom_collide:
            self.yvelocity = self.jumpvelocity
        elif self.yvelocity < self.fallvelocity and not bottom_collide:
            self.yvelocity += 1
        if self.yvelocity > 0 and bottom_collide:
            self.rect.bottom = bottom_collide[0].rect.top
            self.yvelocity = 0
        if self.yvelocity < 0 and top_collide:
            self.rect.top = top_collide[0].rect.bottom
            self.yvelocity = 0
        self.move(self.xvelocity, self.yvelocity)

    def touch(self, x, y, platforms):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.move_ip([-x, -y])
        return collide

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
