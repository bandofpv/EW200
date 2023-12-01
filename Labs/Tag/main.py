# TODO: Finish writing comments for all python files

from player import Player
from timer import Timer
from button import Button
from background import *
from random import choice

# pygame setup
pygame.init()
clock = pygame.time.Clock()

WIDTH = 1080  # screen width
HEIGHT = 620  # screen height

# comment out either screen initializations to set manual size or full screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # create screen surface
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

block_size = (25, 25)
fps = 60
game_time = 5
spawn_interval = 5
longevity = 10

arrow_keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP)
wasd_keys = (pygame.K_d, pygame.K_a, pygame.K_w)

it = choice([True, False])
player1 = Player(screen.get_width() // 3, screen.get_height() - 50, block_size, 'green', wasd_keys, it)
player2 = Player(2 * screen.get_width() // 3, screen.get_height() - 50, block_size, 'blue', arrow_keys, not it)

platforms = pygame.sprite.Group()

collectibles = pygame.sprite.Group()

game_timer = Timer(game_time, screen)

running = True
play = True
started = False
show_cursor = False
spawned = False

start_button = Button(screen.get_rect().center, 'Play', 140, 'white', screen)
play_again_button = Button(screen.get_rect().center, 'Play Again', 120, 'white', screen)
screen_centerx, screen_centery = screen.get_rect().centerx, screen.get_rect().centery
quit_button = Button((screen_centerx, screen_centery + 145), 'Quit', 80, 'white', screen)

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
            build_border(screen, block_size, platforms)
            build_game(block_size, platforms, screen, fps)
            game_timer = Timer(game_time, screen)

    else:
        if play:
            show_cursor = display_cursor(show_cursor, game_events)
            pygame.mouse.set_visible(show_cursor)

            player1.update(platforms, player2, collectibles)
            player2.update(platforms, player1, collectibles)
            platforms.update()
            game_timer.update()
            collectibles.update(longevity)

            if game_timer.timer // 1000 % spawn_interval == 0 and not spawned:
                spawn_collectible(screen, block_size, collectibles)
                spawned = True
            elif game_timer.timer // 1000 % spawn_interval != 0:
                spawned = False

            game_timer.draw()
            collectibles.draw(screen)
            platforms.draw(screen)
            player1.draw(screen)
            player2.draw(screen)

            play = game_timer.play

        else:
            pygame.mouse.set_visible(True)
            play = play_again_button.click(game_events, 1.05)
            display_winner(screen, player1, player2, 120)
            if quit_button.click(game_events, font_color='red'):
                running = False
            player1.kill()
            player2.kill()
            [platform.kill() for platform in platforms]
            [collectible.kill() for collectible in collectibles]
            if play:
                it = choice([True, False])
                player1 = Player(screen.get_width() // 3, screen.get_height() - 50, block_size, 'green',
                                 wasd_keys, it)
                player2 = Player(2 * screen.get_width() // 3, screen.get_height() - 50, block_size, 'blue',
                                 arrow_keys, not it)
                build_border(screen, block_size, platforms)
                build_game(block_size, platforms, screen, fps)
                game_timer = Timer(game_time, screen)
                show_cursor = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
