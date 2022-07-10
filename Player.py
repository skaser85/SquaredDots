from typing import Callable, Dict
import pygame
from dataclasses import dataclass
from Button import Button
from Input import Input

@dataclass
class Player:
    name: str
    color: pygame.Color
    score: int = 0
    active: bool = False

    def draw(self, surface: pygame.Surface, x: int, y: int, ui_font: pygame.font.Font, default_font: pygame.font.Font, m: pygame.Vector2) -> Callable|None:
        hot_action = None
        # draw dot to show if it's this player's turn
        if self.active:
            pygame.draw.ellipse(surface, self.color, pygame.Rect(x - 30, y + 6, 20, 20))
        # draw buttons
        change_name_btn = Button('Change Name', self.change_name, ui_font)
        change_name_btn.draw(surface, x, y - 10, m)
        if change_name_btn.hovered:
            hot_action = change_name_btn.action
        change_color_btn = Button('Change Color', self.change_color, ui_font)
        change_color_btn.draw(surface, change_name_btn.rect.right, y - 10, m)
        if change_color_btn.hovered:
            hot_action = change_color_btn.action
        # draw player's name
        text = default_font.render(f'{self.name}: {self.score}', True, self.color)
        surface.blit(text, (x, y))
        return hot_action

    def set_active(self, is_active: bool) -> None:
        self.active = is_active

    def change_name(self) -> Dict[str, str]:
        return {
            'input_type': 'text',
            'input_title': 'Change Name',
            'initial_value': self.name,
            'player': self
        }

    def change_color(self) -> None:
        print(f'Change color button pressed from {self.name}')