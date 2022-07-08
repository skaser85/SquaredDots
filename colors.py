from __future__ import annotations
from dataclasses import dataclass
import pygame

@dataclass
class Colors:
    BLACK:      pygame.Color = pygame.Color(0,0,0)
    BLUE:       pygame.Color = pygame.Color(0,0,255)
    BLUE2:      pygame.Color = pygame.Color(29, 145, 191)
    DARK_GREY:  pygame.Color = pygame.Color(50,50,50)
    DARK_GREEN: pygame.Color = pygame.Color(5, 163, 63)
    WHITE:      pygame.Color = pygame.Color(255,255,255)
    GREEN:      pygame.Color = pygame.Color(0,255,0,128)
    GREY:       pygame.Color = pygame.Color(128,128,128)
    RED:        pygame.Color = pygame.Color(255,0,0)
    RED2:       pygame.Color = pygame.Color(235,110,110)
    MAGENTA:    pygame.Color = pygame.Color(255,0,255)
    PINK:       pygame.Color = pygame.Color(255,112,200)
    PURPLE:     pygame.Color = pygame.Color(208,105,240)
    CYAN:       pygame.Color = pygame.Color(0,255,255)
    YELLOW:     pygame.Color = pygame.Color(255,255,0)

    @staticmethod
    def copy(color: pygame.Color) -> pygame.Color:
        return pygame.Color(color.r, color.g, color.b, color.a)

    @staticmethod
    def brighten(color: pygame.Color, percent: float = 0.1) -> pygame.Color:
        default_value = 100
        r = default_value if color.r == 0 else min(int(color.r * (1.0 + percent)), 255)
        g = default_value if color.g == 0 else min(int(color.g * (1.0 + percent)), 255)
        b = default_value if color.b == 0 else min(int(color.b * (1.0 + percent)), 255)
        return pygame.Color(r,g,b,color.a)

    @staticmethod
    def darken(color: pygame.Color, percent: float = 0.1) -> pygame.Color:
        # this sucks - figure out a better way
        default_value = 100
        r = default_value if color.r == 255 else min(int(color.r * (1.0 - percent)) + color.r,255)
        g = default_value if color.g == 255 else min(int(color.g * (1.0 - percent)) + color.g,255)
        b = default_value if color.b == 255 else min(int(color.b * (1.0 - percent)) + color.b,255)
        return pygame.Color(r,g,b,color.a)