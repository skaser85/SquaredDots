import pygame
from dataclasses import dataclass
from colors import Colors
from Edge import Edge

@dataclass
class Square:
    top: Edge
    right: Edge
    bottom: Edge
    left: Edge
    padding: int
    rect: pygame.Rect = None
    color: pygame.Color = Colors.YELLOW

    def __post_init__(self):
        left = self.top.dot0.rect.left + self.padding / 2
        top = self.top.dot0.rect.top + self.padding / 2
        d0 = pygame.Vector2(self.top.dot0.rect.centerx, self.top.dot0.rect.centery)
        d1 = pygame.Vector2(self.top.dot1.rect.centerx, self.top.dot1.rect.centery)
        size = d0.distance_to(d1)
        self.rect = pygame.Rect(left, top, size, size)

    def draw(self, surface: pygame.surface):
        pygame.draw.rect(surface, self.color, self.rect)