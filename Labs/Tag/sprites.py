import pygame


# define a class called Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, keys, it):
        super().__init__()
        self.color = color
        self.it = it
        self.it_body = pygame.image.load('assets/images/red_body.png')
        self.it_body = pygame.transform.smoothscale(self.it_body, size)
        self.body = pygame.image.load(f'assets/images/{self.color}_body.png')
        self.body = pygame.transform.smoothscale(self.body, size)
        self.image = self.body
        self.pause = False
        if self.it:
            self.image = self.it_body
            self.pause = True
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.timer = pygame.time.get_ticks()
        self.speed = 3
        self.xvelocity, self.yvelocity = 0, 0
        self.right_key, self.left_key, self.up_key = keys
        self.jumpvelocity = -15
        self.fallvelocity = 10

    def update(self, platforms, opponent):
        top_collide = self.touch(0, self.yvelocity, platforms)
        bottom_collide = self.touch(0, self.fallvelocity, platforms)
        right_collide = self.touch(self.speed, 0, platforms)
        left_collide = self.touch(-self.speed, 0, platforms)
        opponent_collide = pygame.Rect.colliderect(self.rect, opponent.rect)
        update_time = pygame.time.get_ticks()
        if opponent_collide and not self.it and (update_time - self.timer) > 3000:
            self.image = self.it_body
            self.it = True
            self.pause = True
            self.timer = update_time
        if opponent_collide and self.it and (update_time - self.timer) > 3000:
            self.image = self.body
            self.it = False
            self.pause = False
            self.timer = update_time
        if (update_time - self.timer) > 3000:
            self.pause = False
        self.xvelocity = 0
        key = pygame.key.get_pressed()
        if key[self.left_key]:
            if left_collide and self.yvelocity == 0:
                self.rect.left = left_collide.rect.right
            elif not left_collide:
                self.xvelocity = -self.speed
        if key[self.right_key]:
            if right_collide and self.yvelocity == 0:
                self.rect.right = right_collide.rect.left
            elif not right_collide:
                self.xvelocity = self.speed
        if key[self.up_key] and self.yvelocity == 0 and bottom_collide:
            self.yvelocity = self.jumpvelocity
        elif self.yvelocity < self.fallvelocity and not bottom_collide:
            self.yvelocity += 1
        if self.yvelocity > 0 and bottom_collide:
            self.rect.bottom = bottom_collide.rect.top
            self.yvelocity = 0
        if self.yvelocity < 0 and top_collide:
            self.rect.top = top_collide.rect.bottom
            self.yvelocity = 0
        if self.pause:
            self.xvelocity = 0
            self.yvelocity = 0
        self.rect.move_ip(self.xvelocity, self.yvelocity)

    def touch(self, x, y, platforms):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, platforms)
        self.rect.move_ip([-x, -y])
        return collide

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, size, side):
        super().__init__()
        self.image = pygame.image.load(f'assets/images/tile_{side}.png')
        self.image = pygame.transform.smoothscale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
