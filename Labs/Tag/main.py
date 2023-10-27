import pygame
from Sprites import *

# pygame setup
pygame.init()
clock = pygame.time.Clock()

WIDTH = 1080  # screen width
HEIGHT = 608  # screen height
screen = pygame.display.set_mode((WIDTH,HEIGHT))  # create screen object
screen.fill((66, 35, 223))  # fill the surface with blue


player = Player(100, 400)

platforms = pygame.sprite.Group()
for x in range(0, WIDTH, 25):
    platforms.add(Platform(x, 500))

running = True

while running:

    player.update(platforms)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE
    screen.fill((66, 35, 223))
    player.draw(screen)
    platforms.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
