from typing import Callable, List
import pygame
from dataclasses import dataclass, field
from colors import Colors, Color

@dataclass
class DropdownData:
    color: Color

@dataclass
class Dropdown:
    font: pygame.font.Font
    title: str
    options: List[str] = field(default_factory=list)
    width: int = 150
    height: int = 30
    text_color: Color = Colors.WHITE
    bkg_color: Color = Color.brighten(Colors.DARK_GREY, 0.5)
    padding: int = 10
    hovered: bool = False
    active: bool = False
    anim_duration: int = 255
    anim_timer: int = 255
    anim_speed: int = 10
    hot_option: str = ''
    selected_value: str = ''

    def __post_init__(self):
        self.selected_value = self.options[0]

    def draw(self, surface: pygame.Surface, x: int, y: int, m: pygame.Vector2) -> Callable|None:
        hot_action = None

        title = self.font.render(self.title, True, self.text_color.color)
        surface.blit(title, (x, y))

        y += 15

        text = self.font.render(self.selected_value, True, self.text_color.color)
        
        tw, th = text.get_size()
        
        if tw > self.width + self.padding * 2:
            self.width = tw + self.padding * 2
        
        r = pygame.Rect(x, y, self.width, self.height)

        bkg_color = self.bkg_color
        
        self.hovered = self._mouse_is_over(r, m)
        if self.hovered:
            bkg_color = Color.brighten(self.bkg_color, 0.5)
            hot_action = self.set_active
        
        pygame.draw.rect(surface, bkg_color.color, r)
        pygame.draw.rect(surface, self.text_color.color, r, 1)
        
        tx = x + self.padding/2
        ty = y + self.padding/2 + th/2 - 2

        surface.blit(text, (tx, ty))

        if self.active:
            for opt in self.options:
                y += r.h
                r = pygame.Rect(x, y, self.width, self.height)
                bkg_color = self.bkg_color
                if self._mouse_is_over(r, m):
                    self.hot_option = opt
                    hot_action = self.set_hot_option
                    bkg_color = Color.brighten(self.bkg_color, 0.5)
                pygame.draw.rect(surface, bkg_color.color, r)
                pygame.draw.rect(surface, self.text_color.color, r, 1)
                text = self.font.render(opt, True, self.text_color.color)
                tx = x + self.padding/2
                ty = y + self.padding/2 + th/2 - 2
                surface.blit(text, (tx, ty))

        return hot_action

    def _mouse_is_over(self, r: pygame.Rect, m: pygame.Vector2) -> bool:
        return r.collidepoint(m.x, m.y)

    def set_value(self, value: str) -> None:
        if value in self.options:
            self.selected_value = value
        else:
            raise ValueError(f'Value "{value}" is not a valid option!')

    def set_active(self):
        self.active = not self.active

    def set_hot_option(self):
        self.selected_value = self.hot_option
        self.hot_option = ''
        self.active = False
        return DropdownData(Colors.get_color_by_name(self.selected_value))