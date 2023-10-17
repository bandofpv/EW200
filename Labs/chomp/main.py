# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

background = pygame.Surface((WIDTH, HEIGHT))
background.fill((66, 35, 223))
pygame.draw.rect(background, (215,233,123), (0,WIDTH-100, WIDTH, 100))
screen.blit(background, (0,0))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()