import pygame
from Sprites import *

# pygame setup
pygame.init()
WIDTH = 1080  # screen width
HEIGHT = 608  # screen height
screen = pygame.display.set_mode((WIDTH,HEIGHT))  # create screen object

background = pygame.Surface((WIDTH, HEIGHT))  # create surface object
background.fill((66, 35, 223))  # fill the surface with blue
screen.blit(background, (0, 0))

player = pygame.sprite.Group()
player.add(Player(screen, 100, 100))

running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE
    player.update()
    player.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
