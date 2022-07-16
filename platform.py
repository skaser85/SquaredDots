from pygame.constants import RESIZABLE, VIDEORESIZE, MOUSEWHEEL
from pygame.locals import KEYDOWN, QUIT
from Game import Game
import pygame

pygame.init()
clock = pygame.time.Clock()

gameWidth = 800
gameHeight = 600
game = Game(gameWidth, gameHeight)
game.screen = pygame.display.set_mode((gameWidth, gameHeight),RESIZABLE)
game.load_setup("setup.json")

while game.running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            game.keyboard.update(event.key, event.unicode)
        elif event.type == MOUSEWHEEL:
            game.mouse.set_scroll(event.x, event.y)
        elif event.type == VIDEORESIZE:
            old = game.screen
            game.screen = pygame.display.set_mode((event.w,event.h),RESIZABLE)
            game.screen.blit(old,(0,0))
            del old
        elif event.type == QUIT:
            game.running = False

    pos = pygame.mouse.get_pos()
    game.mouse.pos = pygame.Vector2(pos[0], pos[1])
    game.mouse.set_pressed(pygame.mouse.get_pressed(5))
    game.update()
    game.draw()

    pygame.display.flip()

    clock.tick(30)