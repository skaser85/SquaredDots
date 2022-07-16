from __future__ import annotations
from dataclasses import dataclass, fields
from typing import List
import pygame

@dataclass
class Color:
    name: str
    color: pygame.Color

    @staticmethod
    def copy(color: Color) -> Color:
        return Color(color.name, pygame.Color(color.color.r, color.color.g, color.color.b, color.color.a))

    @staticmethod
    def brighten(color: Color, percent: float = 0.1) -> Color:
        default_value = 100
        r = default_value if color.color.r == 0 else min(int(color.color.r * (1.0 + percent)), 255)
        g = default_value if color.color.g == 0 else min(int(color.color.g * (1.0 + percent)), 255)
        b = default_value if color.color.b == 0 else min(int(color.color.b * (1.0 + percent)), 255)
        return Color(color.name, pygame.Color(r,g,b,color.color.a))

    @staticmethod
    def darken(color: pygame.Color, percent: float = 0.1) -> pygame.Color:
        # this sucks - figure out a better way
        default_value = 100
        r = default_value if color.color.r == 255 else min(int(color.color.r * (1.0 - percent)) + color.color.r,255)
        g = default_value if color.color.g == 255 else min(int(color.color.g * (1.0 - percent)) + color.color.g,255)
        b = default_value if color.color.b == 255 else min(int(color.color.b * (1.0 - percent)) + color.color.b,255)
        return Color(color.name, pygame.Color(r,g,b,color.color.a))

@dataclass
class Colors:
    BLACK:      Color = Color('black', pygame.Color(0,0,0))
    BLUE:       Color = Color('blue', pygame.Color(0,0,255))
    BLUE2:      Color = Color('blue2', pygame.Color(29, 145, 191))
    DARK_GREY:  Color = Color('dark grey', pygame.Color(50,50,50))
    DARK_GREEN: Color = Color('dark green', pygame.Color(5, 163, 63))
    WHITE:      Color = Color('white', pygame.Color(255,255,255))
    GREEN:      Color = Color('green', pygame.Color(0,255,0,128))
    GREY:       Color = Color('grey', pygame.Color(128,128,128))
    RED:        Color = Color('red', pygame.Color(255,0,0))
    RED2:       Color = Color('red2', pygame.Color(235,110,110))
    MAGENTA:    Color = Color('magenta', pygame.Color(255,0,255))
    PINK:       Color = Color('pink', pygame.Color(255,112,200))
    PURPLE:     Color = Color('purple', pygame.Color(208,105,240))
    CYAN:       Color = Color('cyan', pygame.Color(0,255,255))
    YELLOW:     Color = Color('yellow', pygame.Color(255,255,0))

    @classmethod
    def get_color_names(cls) -> List[str]:
        return [c.default.name for c in fields(cls)]
    
    @classmethod
    def get_colors(cls) -> List[str]:
        return [c.default for c in fields(cls)]

    @classmethod
    def get_color_by_name(cls, name: str) -> Color:
        return [c for c in cls.get_colors() if c.name.upper() == name.upper()][0]