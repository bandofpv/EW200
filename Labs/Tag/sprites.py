import pygame


# define a class called Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, keys, it):
        super().__init__()
        self.color = color
        self.it = it
        self.it_body = pygame.image.load(f'assets/images/{self.color}_it_body.png')
        self.it_body = pygame.transform.smoothscale(self.it_body, size)
        self.body = pygame.image.load(f'assets/images/{self.color}_body.png')
        self.body = pygame.transform.smoothscale(self.body, size)
        self.image = self.body
        self.pause = False
        self.speed = 3
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collide_timer = pygame.time.get_ticks()
        self.collectable_timer = pygame.time.get_ticks()
        self.collected = False
        self.xvelocity, self.yvelocity = 0, 0
        self.right_key, self.left_key, self.up_key = keys
        self.jumpvelocity = -15
        self.fallvelocity = 10
        if self.it:
            self.image = self.it_body
            self.pause = True
            self.speed = 4
            self.jumpvelocity = -16

    def update(self, platforms, opponent, collectable_group):
        opponent_collide = pygame.Rect.colliderect(self.rect, opponent.rect)
        current_time = pygame.time.get_ticks()
        if opponent_collide and (current_time - self.collide_timer) > 3000:
            if self.it:
                self.it = False
                self.pause = False
                self.speed = 3
                self.jumpvelocity = -15
                self.collide_timer = current_time
                self.image = self.body
            else:
                self.it = True
                self.pause = True
                self.speed = 4
                self.jumpvelocity = -16
                self.collide_timer = current_time
                self.image = self.it_body
        # elif opponent_collide and self.it and (current_time - self.collide_timer) > 3000:
        #     self.it = False
        #     self.pause = False
        #     self.speed = 3
        #     self.collide_timer = current_time
        if (current_time - self.collide_timer) > 3000:
            self.pause = False
        # if self.it:
        #     self.image = self.it_body
        # else:
        #     self.image = self.body
        top_collide = self.touch(0, self.yvelocity, platforms)
        bottom_collide = self.touch(0, self.fallvelocity, platforms)
        right_collide = self.touch(self.speed, 0, platforms)
        left_collide = self.touch(-self.speed, 0, platforms)
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

        collectable = pygame.sprite.spritecollideany(self, collectable_group)
        if collectable and not self.it:
            collectable.kill()
            self.collected = True
            self.speed = 5
            self.jumpvelocity = -17
            self.collectable_timer = current_time
        if self.collected and (current_time - self.collectable_timer) > 3000:
            self.collected = False
            self.speed = 3
            self.jumpvelocity = -15

    def touch(self, x, y, platforms):
        self.rect.move_ip((x, y))
        collide = pygame.sprite.spritecollideany(self, platforms)
        self.rect.move_ip((-x, -y))
        return collide

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, size, side):
        super().__init__()
        self.image = pygame.image.load(f'assets/images/tile_{side}.png')
        self.image = pygame.transform.smoothscale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Collectable(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f'assets/images/tile_exclamation.png')
        self.image = pygame.transform.smoothscale(self.image, [25, 25])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)