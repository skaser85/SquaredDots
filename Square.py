import pygame
from dataclasses import dataclass
from Edge import Edge
from Player import Player
from _math import Vec2

@dataclass
class Square:
    top: Edge
    right: Edge
    bottom: Edge
    left: Edge
    padding: int
    player: Player
    font: pygame.font.Font
    rect: pygame.Rect = None

    def __post_init__(self):
        left = self.top.dot0.rect.centerx
        top = self.top.dot0.rect.centery
        d0 = Vec2(self.top.dot0.rect.centerx, self.top.dot0.rect.centery)
        d1 = Vec2(self.top.dot1.rect.centerx, self.top.dot1.rect.centery)
        size = d0.dist(d1)
        self.rect = pygame.Rect(left, top, size, size)

    def draw(self, surface: pygame.surface):
        pygame.draw.rect(surface, self.player.color.color, self.rect, 3)
        text = self.font.render(self.player.name[0], True, self.player.color.color)
        w = text.get_width()
        h = text.get_height()
        x = self.rect.centerx - w/2 + 3
        y = self.rect.centery - h/2
        surface.blit(text, (x, y))
