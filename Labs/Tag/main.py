# TODO: Finish writing comments for all python files

import pygame
from player import Player
#from collectible import Collectible
from timer import Timer
from button import Button
from background import *

# pygame setup
pygame.init()
clock = pygame.time.Clock()

WIDTH = 1080  # screen width
HEIGHT = 608  # screen height
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # create screen surface
pygame.display.set_caption('TAG!')

block_size = (25, 25)
game_time = 60

arrow_keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP)
wasd_keys = (pygame.K_d, pygame.K_a, pygame.K_w)
player1 = Player(100, 400, block_size, 'green', arrow_keys, True)
player2 = Player(200, 400, block_size, 'blue', wasd_keys, False)

platforms = pygame.sprite.Group()
build_border(screen, block_size, platforms)
build_level(block_size, platforms, screen)

collectibles = pygame.sprite.Group()
collectibles.add(Collectible(500, 500))
collectibles.add(Collectible(400, 500))

game_timer = Timer(game_time, screen)

running = True
play = True
started = False
show_cursor = False

start_button = Button(screen.get_rect().center, 'Play', 120, 'white', screen)
play_again_button = Button(screen.get_rect().center, 'Play Again', 100, 'white', screen)
screen_centerx, screen_centery = screen.get_rect().centerx, screen.get_rect().centery
quit_button = Button((screen_centerx, screen_centery + 145), 'Quit', 60, 'white', screen)

while running:

    screen.fill('black')

    # poll for events
    game_events = pygame.event.get()

    # pygame.QUIT event means the user clicked X to close your window
    for event in game_events:
        if event.type == pygame.QUIT:
            running = False

    if not started:
        started = start_button.click(game_events, 1.1)
        if started:
            player1 = Player(100, 400, block_size, 'green', arrow_keys, True)
            player2 = Player(200, 400, block_size, 'blue', wasd_keys, False)
            build_border(screen, block_size, platforms)
            build_level(block_size, platforms, screen)
            game_timer = Timer(game_time, screen)

    else:
        if play:
            show_cursor = display_cursor(show_cursor, game_events)
            pygame.mouse.set_visible(show_cursor)

            player1.update(platforms, player2, collectibles)
            player2.update(platforms, player1, collectibles)
            platforms.update()
            game_timer.update()

            collectibles.draw(screen)

            player1.draw(screen)
            player2.draw(screen)
            platforms.draw(screen)
            game_timer.draw()

            play = game_timer.play

        else:
            pygame.mouse.set_visible(True)
            play = play_again_button.click(game_events, 1.05)
            display_winner(screen, player1, player2, 100)
            if quit_button.click(game_events, font_color='red'):
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
                show_cursor = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
