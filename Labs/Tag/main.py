import pygame
from sprites import *
from background import *

# pygame setup
pygame.init()
clock = pygame.time.Clock()

WIDTH = 1080  # screen width
HEIGHT = 608  # screen height
screen = pygame.display.set_mode((WIDTH,HEIGHT))  # create screen object

block_size = (25, 25)
game_time = 60

arrow_keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP)
wasd_keys = (pygame.K_d, pygame.K_a, pygame.K_w)
player1 = Player(100, 400, block_size, 'green', arrow_keys, True)
player2 = Player(200, 400, block_size, 'blue', wasd_keys, False)

platforms = pygame.sprite.Group()
build_border(screen, block_size, platforms)
build_level(block_size, platforms, screen)

game_timer = Timer(game_time, screen)

running = True
play = True
started = False

while running:

    screen.fill('black')

    # poll for events
    game_events = pygame.event.get()

    # pygame.QUIT event means the user clicked X to close your window
    for event in game_events:
        if event.type == pygame.QUIT:
            running = False

    if not started:
        started = start_menu(screen, game_events)
        if started:
            player1 = Player(100, 400, block_size, 'green', arrow_keys, True)
            player2 = Player(200, 400, block_size, 'blue', wasd_keys, False)
            build_border(screen, block_size, platforms)
            build_level(block_size, platforms, screen)
            game_timer = Timer(game_time, screen)

    else:
        if play:
            player1.update(platforms, player2)
            player2.update(platforms, player1)
            game_timer.update()

            # RENDER YOUR GAME HERE
            player1.draw(screen)
            player2.draw(screen)
            platforms.draw(screen)
            game_timer.draw()

            play = game_timer.play

        else:
            play = play_again(screen, game_events, (player1.it, player2.it), 100)
            if quit_button(screen, game_events, 50):
                running = False
            player1.kill()
            player2.kill()
            [platform.kill() for platform in platforms]
            if play:
                player1 = Player(100, 400, block_size, 'green', arrow_keys, True)
                player2 = Player(200, 400, block_size, 'blue', wasd_keys, False)
                build_border(screen, block_size, platforms)
                build_level(block_size, platforms, screen)
                game_timer = Timer(game_time, screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
