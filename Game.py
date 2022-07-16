import os
from dataclasses import dataclass, field
from typing import Callable, List, Dict
from json import loads
import pygame
from font import FontStore, FontUseType, _Font, _SysFont
from Menu import Menu
from colors import Colors, Color
from Board import Board
from Player import InputData, Player
from Input import Input
from Dropdown import Dropdown, DropdownData
from Keyboard import Keyboard
from Mouse import Mouse

@dataclass
class Game:
    screen_width: int
    screen_height: int
    font_store: FontStore = FontStore()
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
    background_color: Color = Colors.BLACK
    dragging: bool = False
    hot_action: Callable = None
    board: Board = None
    players: List[Player] = field(default_factory=list)
    active_player_index: int = 0
    _input: Input = None
    player_to_change: Player = None
    _color_names: List[str] = field(default_factory=list)
    menu_actions: Dict[str, Callable] = field(default_factory=dict)
    keyboard: Keyboard = None
    mouse: Mouse = None

    def __post_init__(self):
        pygame.font.init()
        pygame.mixer.init()
        self._color_names = Colors.get_color_names()
        self.menu_actions['start_game'] = self.start_game
        self.menu_actions['quit_game'] = self.quit_game
        self.menu_actions['resume_game'] = self.resume_game
        self.menu_actions['restart_game'] = self.restart_game
        self.keyboard = Keyboard()
        self.mouse = Mouse()

    def set_menu(self, menu_name):
        self.menu = self.menus[menu_name]
        self.menu_item_hot = self.menu.menu_items[self.menu.menu_item_hot_index]

    def create_menu(self, name):
        self.menus[name] = Menu(self.font_store.menu.font)

    def register_sound(self, name, path, volume=0.3):
        if name not in self.sounds.keys():
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(volume)

    def set_background_color(self, color):
        self.background_color = color

    def register_background_image(self, path):        
        self.background_image = pygame.image.load(path)
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

    def register_font(self, path: str, size: int, font_use_type: FontUseType) -> None:
        if font_use_type == FontUseType.DEFAULT:
            self.font_store.default = _Font(path, size)
        elif font_use_type == FontUseType.MENU:
            self.font_store.menu = _Font(path, size)
        elif font_use_type == FontUseType.UI:
            self.font_store.ui = _Font(path, size)
        else:
            raise ValueError(f'Unknown font_use_type: {font_use_type}')

    def register_sys_font(self, font_name: str, size: int, font_use_type: FontUseType) -> None:
        if font_use_type == FontUseType.DEFAULT:
            self.font_store.default = _SysFont(font_name, size)
        elif font_use_type == FontUseType.MENU:
            self.font_store.menu = _SysFont(font_name, size)
        elif font_use_type == FontUseType.UI:
            self.font_store.ui = _SysFont(font_name, size)
        else:
            raise ValueError(f'Unknown font_use_type: {font_use_type}')
    
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
            self.screen.fill(self.background_color.color)
        else:
            self.screen.blit(self.background_image, (0, 0))

        self.hot_action = None
        m = self.mouse.last_pos

        # if we're paused or the game hasn't started yet,
        # then update and draw the menu
        if self.paused or not self.game_started:
            self.menu_active = True
            action = self.menu.draw(self.screen, m)
            if action is not None:
                self.hot_action = action
        else: 
            # draw the game
            if self.menu_active:
                self.menu_active = False
                self.menu.reset()
                self.menu.menu_item_hot = None

            start_x = 35
            if self.board is None:
                start_y = 35
                max_x = self.screen_width - (self.screen_width // 3)
                max_y = self.screen_height - start_y
                self.board = Board(start_x, start_y, max_x, max_y, self.font_store.default.font, self.background_color)
                self.board.set_player(self.players[self.active_player_index])
            self.board.draw(self.screen)
        
            # draw players' text
            x = self.board.rect.right + start_x
            y = 50
            for p in self.players:
                action = p.draw(self.screen, x, y, self.font_store.ui.font, self.font_store.default.font, m)
                if action is not None:
                    self.hot_action = action
                y += 50

            # draw input
            if self._input is not None:
                action = self._input.draw(self.screen, x, y + 100, m)
                if action is not None:
                    self.hot_action = action

    def update(self):
        if self.mouse.left_down:
            self.handle_click()
        if self.board is not None:
            self.board.update(self.mouse.pos)
        if self._input is not None:
            if isinstance(self._input, Input):
                text = self._input.update_text(self.keyboard)
                if text is not None:
                    self.player_to_change.name = text
                    self.player_to_change = None
                    self._input = None
        else:
            if self.keyboard.escape:
                if self.paused:
                    # testing
                    self.running = False
                    # live
                    self.resume_game()
                else:
                    if self.game_started:
                        self.pause_game()
            elif self.keyboard.enter:
                if self.menu.menu_item_hot is not None:
                    self.menu.menu_item_hot.action()
            elif self.keyboard.arrow.up:
                if self.paused:
                    self.menu.select_menu_item(-1)
            elif self.keyboard.arrow.down:
                if self.paused:
                    self.menu.select_menu_item(1)
        self.keyboard = Keyboard()
        self.mouse = Mouse.next_frame(self.mouse)
    
    def handle_click(self):
        if self.hot_action is not None:
            value = self.hot_action()
            if isinstance(value, InputData):
                if value.input_type == 'text':
                    self._input = Input(self.font_store.ui.font, value.input_title, value.initial_value, 10)
                    self.player_to_change = value.player
                elif value.input_type == 'color':
                    self._input = Dropdown(self.font_store.ui.font, value.input_title, self._color_names)
                    self._input.set_value(value.initial_value)
                    self.player_to_change = value.player
                else:
                    ...
            if isinstance(value, DropdownData):
                self.player_to_change.color = value.color
                self.player_to_change = None
                self._input = None
            self.hot_action = None
        else:
            move_made, squares_completed = self.board.handle_click()
            if squares_completed > 0:
                self.players[self.active_player_index].score += squares_completed
            if move_made and not squares_completed:
                self.players[self.active_player_index].set_active(False)
                self.active_player_index += 1
                if self.active_player_index == len(self.players):
                    self.active_player_index = 0
                self.players[self.active_player_index].set_active(True)
                self.board.set_player(self.players[self.active_player_index])
                self.board.clear_available()
                self.board.deselect_dot()

    def load_setup(self, setup_file_path: str) -> None:
        with open(setup_file_path) as f:
            data = loads(f.read())
        # set background
        if len(data['backgroundColor']) > 0:
            self.set_background_color(Colors.get_color_by_name(data['backgroundColor']))
        elif len(data['backgroundImagePath']) > 0:
            self.register_background_image(data['backgroundImagePath'])
        #set fonts
        for font_type in data['fonts']:
            font = data['fonts'][font_type]
            font_use_type = FontUseType.get_by_name(font_type)
            if font['sysFont']:
                self.register_sys_font(font['name'], font['size'], font_use_type)
            else:
                self.register_font(os.path.join(data['assetsPath'], 'Fonts', f'{font["name"]}.ttf'), font['size'], font_use_type)
        # set menus
        for menu in data['menus']:
            self.create_menu(menu['title'])
            for item in menu['items']:
                action = None
                if item['action'] in self.menu_actions:
                    action = self.menu_actions[item['action']]
                self.menus[menu['title']].add_menu_item(item['title'], action)
        self.set_menu(data['startMenu'])
        # add players
        for i, player in enumerate(data['players']):
            p = Player(player['name'], Colors.get_color_by_name(player['color']))
            if i == 0:
                p.active = True
            self.players.append(p)