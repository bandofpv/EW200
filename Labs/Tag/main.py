import pygame
from sprites import *
from background import *

# pygame setup
pygame.init()
clock = pygame.time.Clock()

WIDTH = 1080  # screen width
HEIGHT = 608  # screen height
screen = pygame.display.set_mode((WIDTH,HEIGHT))  # create screen object
screen.fill('black')  # fill the surface with blue

block_size = (25, 25)

arrow_keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP)
wasd_keys = (pygame.K_d, pygame.K_a, pygame.K_w)
player1 = Player(100, 400, block_size, 'green', arrow_keys, True)
player2 = Player(200, 400, block_size, 'blue', wasd_keys, False)

platforms = pygame.sprite.Group()
build_border(screen, block_size, platforms)
build_platform(600, 500, block_size, 300, platforms, screen)
build_platform(400, 400, block_size,  200, platforms, screen)
build_platform(200, 300, block_size,  200, platforms, screen)
build_platform(700, 200, block_size,  8000, platforms, screen)

game_timer = Timer(screen)
#menu = Menu(screen)

running = True
play = True

while running:

    game_events = pygame.event.get()

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in game_events:
        if event.type == pygame.QUIT:
            running = False

    if play:
        player1.update(platforms, player2)
        player2.update(platforms, player1)
        game_timer.update()

        # RENDER YOUR GAME HERE
        screen.fill('black')
        player1.draw(screen)
        player2.draw(screen)
        platforms.draw(screen)
        game_timer.draw()

        play = game_timer.play

    else:
        screen.fill('black')
        player1.kill()
        player2.kill()
        [platform.kill() for platform in platforms]
        play = play_again(screen, game_events)
        if play:
            player1 = Player(100, 400, block_size, 'green', arrow_keys, True)
            player2 = Player(200, 400, block_size, 'blue', wasd_keys, False)
            build_border(screen, block_size, platforms)
            build_platform(600, 500, block_size, 300, platforms, screen)
            build_platform(400, 400, block_size, 200, platforms, screen)
            build_platform(200, 300, block_size, 200, platforms, screen)
            build_platform(700, 200, block_size, 8000, platforms, screen)
            game_timer = Timer(screen)
        # menu.update()
        # menu.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
