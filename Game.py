from typing import Callable, List, Dict
from random import choice
import pygame
from pygame.color import Color
from Menu import Menu
from colors import Colors
from Board import Board

class Game():
    def __init__(self, screen_width, screen_height):
        pygame.font.init()
        pygame.mixer.init()
        self.font: pygame.font.Font = None
        self.score: int = 0
        self.game_started: bool = False
        self.screen: pygame.display = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.running: bool = True
        self.paused: bool = True
        self.all_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.sounds: dict = {}
        self.menus: dict = {}
        self.menu: Menu = None
        self.menu_active: Menu = False
        self.game_has_run_once: bool = False
        self.background_image: pygame.image = None
        self.background_color: pygame.Color = Colors.BLACK
        self.dragging: bool = False
        self.hot_action: Callable = None

        self.board: Board = None

    def set_menu(self, menu_name):
        self.menu = self.menus[menu_name]
        self.menu_item_hot = self.menu.menu_items[self.menu.menu_item_hot_index]

    def create_menu(self, name):
        self.menus[name] = Menu(self.screen, self.font)

    def register_sound(self, name, path, volume=0.3):
        if name not in self.sounds.keys():
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(volume)

    def set_background_color(self, color):
        self.background_color = color

    def register_background_image(self, path):        
        self.background_image = pygame.image.load(path)
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

    def register_font(self, path, size):
        self.font = pygame.font.Font(path, size)
    
    def register_music(self, path, volume=0.3):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)

    def play_music(self):
        pygame.mixer.music.play(loops=-1)

    def start_game(self):
        self.game_started = True
        self.paused = False
        self.game_has_run_once = True

    def quit_game(self):
        self.running = False

    def pause_game(self):
        self.paused = True
        self.set_menu('pause')

    def resume_game(self):
        self.paused = False

    def restart_game(self):
        self.game_started = True
        self.paused = False
        self.score = 0

    def draw(self):
        # clear the screen
        if self.background_image is None:
            self.screen.fill(self.background_color)
        else:
            self.screen.blit(self.background_image, (0, 0))

        # if we're paused or the game hasn't started yet,
        # then update and draw the menu
        if self.paused or not self.game_started:
            self.menu_active = True
            self.menu.update()
            self.menu.draw()
        else: 
            # draw the game
            if self.menu_active:
                self.menu_active = False
                self.menu.reset()
                self.menu.menu_item_hot = None

            if self.board is None:
                self.board = Board(50, 50, 5, 5)
            self.board.draw(self.screen)

    def update(self):
        if self.board is not None:
            self.board.update(self.get_mouse_pos())
    
    def handle_click(self):
        if self.hot_action is not None:
            self.hot_action()
        else:
            self.board.handle_click()

    def get_mouse_pos(self) -> pygame.Vector2:
        m = pygame.mouse.get_pos()
        return pygame.Vector2(m[0], m[1])