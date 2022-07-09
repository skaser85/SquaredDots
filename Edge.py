import pygame
from dataclasses import dataclass
from enum import Enum, auto
from Dot import Dot
from colors import Colors

class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()

@dataclass
class Edge:
    dot0: Dot
    dot1: Dot
    color: pygame.Color
    direction: Direction = None
    part_of_completed_square: bool = False

    def __post_init__(self):
        if self.dot0.row == self.dot1.row:
            self.direction = Direction.HORIZONTAL
        elif self.dot0.col == self.dot1.col:
            self.direction = Direction.VERTICAL
        else:
            raise ValueError('Cannot determine direction of Edge!')

    def draw(self, surface: pygame.surface):
        pygame.draw.line(surface, self.color, self.dot0.rect.center, self.dot1.rect.center)