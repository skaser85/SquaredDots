from typing import Callable, Any
import pygame
from dataclasses import dataclass
from colors import Colors, Color
from Keyboard import Keyboard

@dataclass
class Cursor:
    height: int
    anim_duration: int = 255
    anim_timer: int = 255
    anim_speed: int = 10
    anim_start_color: Color = None
    anim_target_color: Color = None

    def draw(self, surface: pygame.Surface, x: int, y: int, cursor_color: Color, bkg_color: Color) -> None:
        if self.anim_start_color == None or self.anim_target_color == None:
            self.anim_start_color = cursor_color
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
        pygame.draw.line(surface, c, (x, y), (x, self.height))

@dataclass
class Input:
    font: pygame.font.Font
    title: str
    text: str = ''
    max_len: int = 20
    width: int = 150
    height: int = 30
    text_color: Color = Colors.WHITE
    bkg_color: Color = Color.brighten(Colors.DARK_GREY, 0.5)
    padding: int = 10
    hovered: bool = False
    active: bool = True
    cursor: Cursor = None
    cursor_last_char_past: int = 0
    move_left: bool = False
    move_right: bool = False

    def draw(self, surface: pygame.Surface, x: int, y: int, m: pygame.Vector2) -> Callable|None:
        hot_action = None

        title = self.font.render(self.title, True, self.text_color.color)
        surface.blit(title, (x, y))

        y += 15

        text = self.font.render(self.text, True, self.text_color.color)
        
        tw, th = text.get_size()
        
        if tw > self.width - (self.padding * 2):
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
            if self.cursor is None:
                self.cursor = Cursor(r.bottom - self.padding/1.5)
                self.cursor_last_char_past = len(self.text)
            if len(self.text) == 0:
                cursor_x = tx + self.padding / 2
                self.cursor_last_char_past = 0
            else:
                _text = self.font.render(self.text[:self.cursor_last_char_past], True, self.text_color.color)
                cursor_x = tx + _text.get_width()
            cursor_y = y + self.padding/1.5
            self.cursor.draw(surface, cursor_x, cursor_y, self.text_color, bkg_color)

        return hot_action

    def _mouse_is_over(self, r: pygame.Rect, m: pygame.Vector2) -> bool:
        return r.collidepoint(m.x, m.y)

    def set_active(self):
        self.active = True

    def update_text(self, kb: Keyboard) -> str:
        text = None
        if kb.backspace:
            self.text = self.text[:-1]
        elif kb.space:
            self.text += ' '
            self.cursor_last_char_past += 1
        elif kb.enter or kb.escape:
            if len(self.text) == 0:
                return
            self.active = False
            text = self.text
        elif kb.arrow.left:
            if len(self.text) > 0:
                if self.cursor_last_char_past > 0:
                    self.cursor_last_char_past -= 1
        elif kb.arrow.right:
            if len(self.text) > 0:
                if self.cursor_last_char_past < len(self.text):
                    self.cursor_last_char_past += 1
        else:
            if kb.key is not None and len(self.text) < self.max_len:
                self.text += kb.key
                self.cursor_last_char_past += 1
        return text