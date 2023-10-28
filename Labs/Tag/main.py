import pygame
from Sprites import *

# pygame setup
pygame.init()
clock = pygame.time.Clock()

WIDTH = 1080  # screen width
HEIGHT = 608  # screen height
screen = pygame.display.set_mode((WIDTH,HEIGHT))  # create screen object
screen.fill('black')  # fill the surface with blue

arrow_keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP)
wasd_keys = (pygame.K_d, pygame.K_a, pygame.K_w)
player1 = Player(100, 400, 'green', arrow_keys)
player2 = Player(200, 400, 'blue', wasd_keys)

platforms = pygame.sprite.Group()
for x in range(0, WIDTH, 25):
    platforms.add(Platform(x, 500))

for x in range(400, 600, 25):
    platforms.add(Platform(x, 400))

for x in range(700, 900, 25):
    platforms.add(Platform(x, 475))

running = True

while running:

    player1.update(platforms)
    player2.update(platforms)

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
