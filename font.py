from dataclasses import dataclass, field
from enum import Enum, auto
import pygame

class FontUseType(Enum):
    DEFAULT = auto()
    MENU = auto()
    UI = auto()

@dataclass
class _Font:
    file_path: str
    size: int
    font: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self.set_font(self.file_path, self.size)

    def set_font(self, file_path: str, size: str):
        self.font = pygame.font.Font(file_path, size)

@dataclass
class _SysFont:
    font_name: str
    size: int
    font: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self.set_font(self.font_name, self.size)

    def set_font(self, font_name: str, size: str):
        self.font = pygame.font.SysFont(font_name, size)

@dataclass
class FontStore:
    default: _Font | _SysFont = None
    menu: _Font | _SysFont = None
    ui: _Font | _SysFont = None