from dataclasses import dataclass, field
from typing import Callable, List, Dict
from random import choice
import pygame
from pygame.color import Color
from Menu import Menu
from colors import Colors
from Board import Board
from Player import Player

@dataclass
class Game:
    screen_width: int
    screen_height: int
    font: pygame.font.Font = None
    score: int = 0
    game_started: bool = False
    screen: pygame.display = None
    running: bool = True
    paused: bool = True
    all_sprites: pygame.sprite.Group = pygame.sprite.Group()
    sounds: dict = field(default_factory=dict)
    menus: dict = field(default_factory=dict)
    menu: Menu = None
    menu_active: Menu = False
    game_has_run_once: bool = False
    background_image: pygame.image = None
    background_color: pygame.Color = Colors.BLACK
    dragging: bool = False
    hot_action: Callable = None
    board: Board = None
    players: List[Player] = field(default_factory=list)
    active_player_index: int = 0

    def __post_init__(self):
        pygame.font.init()
        pygame.mixer.init()

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
        p1 = Player('Bilbo', Colors.PURPLE)
        self.players.append(p1)
        p2 = Player('Gollum', Colors.YELLOW)
        self.players.append(p2)

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
                self.board = Board(35, 35, 30, 30, self.font)
                self.board.set_player(self.players[self.active_player_index])
            self.board.draw(self.screen)

            x = self.screen_width - 200
            y = 50
            for i, p in enumerate(self.players):
                if i == self.active_player_index:
                    pygame.draw.ellipse(self.screen, p.color, pygame.Rect(x - 30, y + 6, 20, 20))
                text = self.font.render(f'{p.name}: {p.score}', True, p.color)
                self.screen.blit(text, (x, y))
                y += 30


    def update(self):
        if self.board is not None:
            self.board.update(self.get_mouse_pos())
    
    def handle_click(self):
        if self.hot_action is not None:
            self.hot_action()
        else:
            move_made, squares_completed = self.board.handle_click()
            if squares_completed > 0:
                self.players[self.active_player_index].score += squares_completed
            if move_made and not squares_completed:
                self.active_player_index += 1
                if self.active_player_index == len(self.players):
                    self.active_player_index = 0
                self.board.set_player(self.players[self.active_player_index])
                self.board.clear_available()
                self.board.deselect_dot()

    def get_mouse_pos(self) -> pygame.Vector2:
        m = pygame.mouse.get_pos()
        return pygame.Vector2(m[0], m[1])