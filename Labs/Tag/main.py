import pygame
from sprites import *

# pygame setup
pygame.init()
clock = pygame.time.Clock()

WIDTH = 1080  # screen width
HEIGHT = 608  # screen height
screen = pygame.display.set_mode((WIDTH,HEIGHT))  # create screen object
screen.fill('black')  # fill the surface with blue

arrow_keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP)
wasd_keys = (pygame.K_d, pygame.K_a, pygame.K_w)
player1 = Player(100, 400, 'green', arrow_keys, True)
player2 = Player(200, 400, 'blue', wasd_keys, False)


def build_platform(x, y, length):
    # TODO add if for when length too long
    if x + length > WIDTH:
        length = length - ((x + length) - WIDTH)
    for i in range(x+25, x+length-25, 25):
        platforms.add(Platform(i, y, 'center'))
    platforms.add(Platform(x, y, 'left'))
    platforms.add(Platform(x+length-25, y, 'right'))


platforms = pygame.sprite.Group()

build_platform(0, 500, WIDTH)
build_platform(400, 400, 200)
build_platform(200, 300, 200)
build_platform(700, 200, 800)

# for x in range(400, 600, 25):
#     platforms.add(Platform(x, 400))
#
# for x in range(200, 400, 25):
#     platforms.add(Platform(x, 300))
#
# for x in range(700, 900, 25):
#     platforms.add(Platform(x, 475))

running = True

while running:

    player1.update(platforms, player2)
    player2.update(platforms, player1)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE
    screen.fill('black')
    player1.draw(screen)
    player2.draw(screen)
    platforms.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
