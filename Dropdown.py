from typing import Callable, List
import pygame
from dataclasses import dataclass, field
from colors import Colors, Color

def lerp(a: float, b: float, f: float) -> float:
    return a + f * (b - a)

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
    anim_duration: int = 500
    anim_timer: int = 500
    anim_speed: int = 75
    hot_option: str = ''
    selected_value: str = ''
    transitioning: bool = False
    opened: bool = False

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
        
        input_box = pygame.draw.rect(surface, bkg_color.color, r)
        pygame.draw.rect(surface, self.text_color.color, r, 1)
        
        view_box_top = input_box.bottom
        view_box_bottom = (len(self.options) * self.height) + view_box_top
        
        tx = x + self.padding/2
        ty = y + self.padding/2 + th/2 - 2

        surface.blit(text, (tx, ty))

        view_top = view_box_bottom
        view_bottom = view_box_top
        opening = self.opened
        if self.transitioning:
            if self.transitioning:
                self.anim_timer -= self.anim_speed
                if self.anim_timer <= 0:
                    self.anim_timer = self.anim_duration
                    self.transitioning = False
                else:
                    view_top = lerp(view_box_bottom, view_box_top, (self.anim_timer / self.anim_duration))
                    view_bottom = lerp(view_box_top, view_box_bottom, (self.anim_timer / self.anim_duration))
        
        y += r.h
        hot_action = self.draw_options(opening, surface, x, y, m, view_top, view_bottom, th, hot_action)

        return hot_action

    def draw_options(self, opening: bool, surface: pygame.Surface, x: int, y: int, m: pygame.Vector2, view_top: int, view_bottom: int, th: int, hot_action: Callable) -> Callable:
        for opt in self.options:
            r = pygame.Rect(x, y, self.width, self.height)
            bkg_color = self.bkg_color

            if self._mouse_is_over(r, m):
                # this check is here so that the Dropdown won't pick up on
                # whether we're hovering over something while in transition - 
                # this is done so that we can't set an option hot while the 
                # Dropdown is opening or closing - which causes weirdness
                if not self.transitioning and self.opened:
                    self.hot_option = opt
                    hot_action = self.set_hot_option
                    bkg_color = Color.brighten(self.bkg_color, 0.5)
                
            if self.opened and not self.transitioning:
                self.draw_option(surface, x, y, bkg_color, r, opt, th)
            else:
                if self.transitioning:
                    check_val = view_top if opening else view_bottom
                    if y <= check_val:
                        self.draw_option(surface, x, y, bkg_color, r, opt, th)
            y += r.h
        return hot_action

    def draw_option(self, surface: pygame.Surface, x: int, y: int, bkg_color: Color, r: pygame.Rect, opt: str, th: int) -> None:
        pygame.draw.rect(surface, bkg_color.color, r)
        pygame.draw.rect(surface, self.text_color.color, r, 1)
        text = self.font.render(opt, True, self.text_color.color)
        tx = x + self.padding/2
        ty = y + self.padding/2 + th/2 - 2
        surface.blit(text, (tx, ty))

    def _mouse_is_over(self, r: pygame.Rect, m: pygame.Vector2) -> bool:
        return r.collidepoint(m.x, m.y)

    def set_value(self, value: str) -> None:
        if value in self.options:
            self.selected_value = value
        else:
            raise ValueError(f'Value "{value}" is not a valid option!')

    def set_active(self):
        self.opened = not self.opened
        self.transitioning = not self.transitioning

    def set_hot_option(self):
        self.selected_value = self.hot_option
        self.hot_option = ''
        return DropdownData(Colors.get_color_by_name(self.selected_value))