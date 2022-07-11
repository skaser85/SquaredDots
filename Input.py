from typing import Callable, Any
import pygame
from dataclasses import dataclass
from colors import Colors, Color

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_BACKSPACE,
    K_SPACE,
    K_RETURN
)

@dataclass
class Input:
    font: pygame.font.Font
    title: str
    text: str = ''
    width: int = 150
    height: int = 30
    text_color: Color = Colors.WHITE
    bkg_color: Color = Color.brighten(Colors.DARK_GREY, 0.5)
    padding: int = 10
    hovered: bool = False
    active: bool = True
    anim_duration: int = 255
    anim_timer: int = 255
    anim_speed: int = 10
    anim_start_color: Color = None
    anim_target_color: Color = None

    def draw(self, surface: pygame.Surface, x: int, y: int, m: pygame.Vector2) -> Callable|None:
        hot_action = None

        title = self.font.render(self.title, True, self.text_color.color)
        surface.blit(title, (x, y))

        y += 15

        text = self.font.render(self.text, True, self.text_color.color)
        
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
            cursor_x = tx if len(self.text) == 0 else tx + tw
            cursor_x += 1
            cursor_y = y + self.padding/1.5
            if self.anim_start_color == None or self.anim_target_color == None:
                self.anim_start_color = self.text_color
                self.anim_target_color = bkg_color
            self.anim_timer -= self.anim_speed
            self.anim_timer = max(self.anim_timer, 0)
            if self.anim_timer == 0:
                self.anim_timer = self.anim_duration
                temp = Color.copy(self.anim_start_color)
                self.anim_start_color = Color.copy(self.anim_target_color)
                self.anim_target_color = temp
            lerp_amt = self.anim_timer / self.anim_duration
            c = Color.copy(self.anim_start_color).color.lerp(self.anim_target_color.color, lerp_amt)
            pygame.draw.line(surface, c, (cursor_x, cursor_y), (cursor_x, r.bottom - self.padding/1.5))

        return hot_action

    def _mouse_is_over(self, r: pygame.Rect, m: pygame.Vector2) -> bool:
        return r.collidepoint(m.x, m.y)

    def set_active(self):
        self.active = True

    def update_text(self, key: Any) -> str:
        text = None
        if key == K_BACKSPACE:
            self.text = self.text[:-1]
        elif key == K_SPACE:
            self.text += ' '
        elif key == K_RETURN:
            if len(self.text) == 0:
                return
            self.active = False
            text = self.text
        else:
            self.text += key
        return text