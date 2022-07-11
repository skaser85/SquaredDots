from typing import List, Callable
from dataclasses import dataclass, field
import pygame
from colors import Colors, Color

@dataclass
class MenuItem():
    font: pygame.font.Font
    txt: str
    action: Callable
    is_hot: bool = False

# Define Menu class
@dataclass
class Menu():
    font: pygame.font.Font
    menu_items: List[MenuItem] = field(default_factory=list)
    menu_item_gap: int = 50
    menu_item_hot: MenuItem = None
    menu_item_hot_index: int = 0
    menu_item_color: Color = Colors.WHITE
    menu_item_hot_color: Color = Colors.YELLOW
    anim_duration: int = 255
    anim_timer: int = 255
    anim_speed: int = 10
    anim_start_color: Color = Colors.WHITE
    anim_target_color: Color = Colors.YELLOW

    def get_hot_item(self) -> MenuItem:
        return self.menu_item_hot

    def add_menu_item(self, txt: str, action: Callable) -> None:
        mi = MenuItem(self.font, txt, action)
        self.menu_items.append(mi)
        if self.menu_item_hot is None:
            self.menu_item_hot = self.menu_items[0]
            self.menu_items[0].is_hot = True

    def select_menu_item(self, direction: int) -> None:
        if direction < 0 and self.menu_item_hot == self.menu_items[0]:
            return
        if direction > 0 and self.menu_item_hot == self.menu_items[-1]:
            return
        else:
             self.menu_item_hot_index += direction
             if self.menu_item_hot is not None:
                 self.menu_item_hot.is_hot = False
             self.menu_item_hot = self.menu_items[self.menu_item_hot_index]
             self.menu_item_hot.is_hot = True

    def reset(self):
        self.menu_item_hot_index = 0
        if self.menu_item_hot:
            self.menu_item_hot.is_hot = False
        self.menu_item_hot = self.menu_items[self.menu_item_hot_index]
        self.menu_item_hot.is_hot = True
    
    def draw(self, surface: pygame.Surface, m: pygame.Vector2) -> Callable|None:
        hot_action = None
        
        screen_width, screen_height = surface.get_size()
        text = self.font.render(self.menu_items[0].txt, True, self.menu_item_color.color)
        text_height = text.get_height()
        sum_text_height = text_height * len(self.menu_items)
        sum_gaps_height = self.menu_item_gap * (len(self.menu_items) - 1)
        total_height = sum_text_height + sum_gaps_height
        y_start = (screen_height/2) - (total_height/2)
        
        for idx, item in enumerate(self.menu_items):
            y_offset = y_start + (self.menu_item_gap * idx)
            text = self.font.render(item.txt, True, self.menu_item_color.color)
            tw, th = text.get_size()
            tx = screen_width / 2 - tw / 2
            ty = y_offset
            r = pygame.Rect(tx, ty, tw, th)
            if item.is_hot:
                was_hot_r = r
            item.is_hot = self._mouse_is_over(r, m)
            if item.is_hot:
                
                self.anim_timer -= self.anim_speed
                self.anim_timer = max(self.anim_timer, 0)
                if self.anim_timer == 0:
                    self.anim_timer = self.anim_duration
                    temp = Color.copy(self.anim_start_color)
                    self.anim_start_color = Color.copy(self.anim_target_color)
                    self.anim_target_color = temp
                lerp_amt = self.anim_timer / self.anim_duration
                c = Color.copy(self.anim_start_color).color.lerp(self.anim_target_color.color, lerp_amt)

                text = self.font.render(item.txt, True, c)
                hot_action = item.action
                if self.menu_item_hot is None:
                    self.menu_item_hot = item
                    self.menu_item_hot_index = idx
                else:
                    if self.menu_item_hot != item:
                        self.menu_item_hot.is_hot = False
                        self.menu_item_hot = item
                        self.menu_item_hot_index = idx
            surface.blit(text, (tx, ty))

        if hot_action is None:
            text = self.font.render(self.menu_item_hot.txt, True, self.menu_item_hot_color.color)
            surface.blit(text, (was_hot_r.left, was_hot_r.top))
            hot_action = self.menu_item_hot.action
            self.menu_item_hot.is_hot = True

        return hot_action

    def _mouse_is_over(self, r: pygame.Rect, m: pygame.Vector2) -> bool:
        return r.collidepoint(m.x, m.y)