import os

# Import the pygame module
import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION, RESIZABLE, VIDEORESIZE

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_ESCAPE,
    K_BACKSPACE,
    K_SPACE,
    K_RETURN,
    K_LSHIFT,
    K_LCTRL,
    K_LALT,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYUP,
    KEYDOWN,
    MOUSEBUTTONUP,
    QUIT
)

# Import custom objects
from Game import Game
from font import FontUseType
from colors import Colors

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

gameWidth = 1200
gameHeight = 960
game = Game(gameWidth, gameHeight)
game.screen = pygame.display.set_mode((gameWidth, gameHeight),RESIZABLE)

# register assets
assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
game.register_font(os.path.join(assets_path, 'Fonts', 'kenvector_future_thin.ttf'), 28, FontUseType.DEFAULT)
game.register_font(os.path.join(assets_path, 'Fonts', 'kenvector_future_thin.ttf'), 28, FontUseType.MENU)
game.register_sys_font('consolas', 12, FontUseType.UI)
game.set_background_color(Colors.DARK_GREY)

# create menus
game.create_menu('main')
game.menus['main'].add_menu_item('START GAME', game.start_game)
game.menus['main'].add_menu_item('QUIT GAME', game.quit_game)

game.create_menu('pause')
game.menus['pause'].add_menu_item('RESUME GAME', game.resume_game)
game.menus['pause'].add_menu_item('RESTART GAME', game.restart_game)
game.menus['pause'].add_menu_item('QUIT GAME', game.quit_game)

game.create_menu('restart')
game.menus['restart'].add_menu_item('RESTART GAME', game.restart_game)
game.menus['restart'].add_menu_item('QUIT GAME', game.quit_game)

game.set_menu('main')

# game.play_music()

# Main loop
while game.running:
    # Look at every event in the game
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                game.update(K_BACKSPACE)
            elif event.key in [K_LALT, K_LCTRL, K_LSHIFT]:
                ...
            elif event.key == K_RETURN:
                game.update(K_RETURN)
            elif event.key == K_SPACE:
                game.update(K_SPACE)
            else:
                game.update(event.unicode)
        if event.type == KEYUP:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                if game.paused:
                    # testing
                    game.running = False
                    # live
                    # game.resume_game()
                else:
                    # only pause game if the game is actually running
                    if game.game_started:
                        game.pause_game()
            elif event.key == K_SPACE:
                if game.game_started and (not game.paused):
                    ...
            elif event.key == K_RETURN:
                if game.menu.menu_item_hot is not None:
                    game.menu.menu_item_hot.action()
            elif event.key == K_UP:
                if not game.paused:
                    game.update(K_UP)
                else:
                    game.menu.select_menu_item(-1)
            elif event.key == K_DOWN:
                if not game.paused:
                    game.update(K_DOWN)
                else:
                    game.menu.select_menu_item(1)
            elif event.key == K_LEFT:
                if not game.paused:
                    game.update(K_LEFT)
            elif event.key == K_RIGHT:
                if not game.paused:
                    game.update(K_RIGHT)
        # Handle left mouse button click
        elif event.type == MOUSEBUTTONUP:
            if game.menu.menu_item_hot:
                game.menu.menu_item_hot.action()
            else:
                game.handle_click()
        elif event.type == MOUSEBUTTONDOWN:
            ...
        elif event.type == MOUSEMOTION:
            ...
        elif event.type == VIDEORESIZE:
            old = game.screen
            game.screen = pygame.display.set_mode((event.w,event.h),RESIZABLE)
            game.screen.blit(old,(0,0))
            del old
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            game.running = False

    game.update()
    game.draw()

    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()