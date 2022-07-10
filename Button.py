from __future__ import annotations
from typing import Callable, Tuple
import pygame
from dataclasses import dataclass
from colors import Colors

@dataclass
class Button:
    text: str
    action: Callable
    font: pygame.font.Font
    draw_text_only: bool = True
    text_color: pygame.Color = Colors.WHITE
    bkg_color: pygame.Color = None
    padding: int = 10
    rect: pygame.Rect = None
    hovered: bool = False

    def draw(self, surface: pygame.Surface, x: int, y: int, m: pygame.Vector2):
        text = self.font.render(self.text, True, self.text_color)
        tw, th = text.get_size()
        tx = x
        ty = y
        if self.rect == None:
            w = tw + self.padding * 2
            h = th + self.padding * 2
            self.rect = pygame.Rect(x, y, w, h)
        if not self.draw_text_only:
            self.hovered = self._mouse_is_over(self.rect, m)
        else:
            r = pygame.Rect(x, y, tw, th)
            self.hovered = self._mouse_is_over(r, m)
        if self.hovered:
            text = self.font.render(self.text, True, Colors.CYAN)
        if not self.draw_text_only:
            pygame.draw.rect(surface, self.bkg_color, self.rect)
            tx = x + self.padding
            ty = y + self.padding
        surface.blit(text, (tx, ty))

    def _mouse_is_over(self, r: pygame.Rect, m: pygame.Vector2) -> bool:
        return r.collidepoint(m.x, m.y)