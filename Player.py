import pygame
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    color: pygame.Color
    score: int = 0