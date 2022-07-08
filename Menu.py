from typing import Any, Tuple
import pygame

Color = Tuple[int, int, int]
BLACK: Color = (0,0,0)
WHITE: Color = (255,255,255)
YELLOW: Color = (255, 255, 0)

class Menu_Item():
    def __init__(self, font, txt, action):
        self.font = font
        self.txt = txt
        self.action = action
        self.color = WHITE
        self.rendered_text = self.font.render(self.txt, True, self.color)
        self.rendered_rect = None
        self.is_hot = False
        self.x = 0
        self.y = 0

    def set_rendered_text(self):
        self.rendered_text = self.font.render(self.txt, True, self.color)

    def set_hot(self):
        self.is_hot = True
        self.color = YELLOW

    def unset_hot(self):
        self.is_hot = False
        self.color = WHITE

    def update(self, screen_width, screen_height, y_start):
        rt_x, rt_y = self.rendered_text.get_size()
        self.x = (screen_width/2) - (rt_x/2)
        self.y = y_start
        w = self.rendered_text.get_rect().width
        h = self.rendered_text.get_rect().height
        mx, my = pygame.mouse.get_pos()
        if mx > self.x and mx < self.x + w and my > self.y and my < self.y + h:
            self.set_hot()

# Define Menu class
class Menu():
    def __init__(self, screen, font):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.font = font
        self.menu_items = []
        self.menu_item_offset = 0
        self.menu_item_gap = 50
        self.menu_item_hot = None
        self.menu_item_hot_index = 0

    def get_hot_item(self):
        return self.menu_item_hot

    def add_menu_item(self, txt, action):
        self.menu_items.append(Menu_Item(self.font, txt, action))
        if self.menu_item_hot is None:
            self.menu_item_hot = self.menu_items[0]
            self.menu_items[0].set_hot()

    def select_menu_item(self, direction):
        if direction < 0 and self.menu_item_hot == self.menu_items[0]:
            return
        if direction > 0 and self.menu_item_hot == self.menu_items[-1]:
            return
        else:
             self.menu_item_hot_index += direction
             if self.menu_item_hot is not None:
                 self.menu_item_hot.unset_hot()
             self.menu_item_hot = self.menu_items[self.menu_item_hot_index]
             self.menu_item_hot.set_hot()

    def update(self):
        text_height = self.menu_items[0].rendered_text.get_height()
        sum_text_height = text_height * len(self.menu_items)
        sum_gaps_height = self.menu_item_gap * (len(self.menu_items) - 1)
        total_height = sum_text_height + sum_gaps_height
        y_start = (self.screen_height/2) - (total_height/2)
        for idx, item in enumerate(self.menu_items):
            y_offset = y_start + (self.menu_item_gap * idx)
            item.update(self.screen_width, self.screen_height, y_offset)
            item.set_rendered_text()
            if item.is_hot:
                if self.menu_item_hot is None:
                    self.menu_item_hot = item
                    self.menu_item_hot_index = idx
                else:
                    if self.menu_item_hot != item:
                        self.menu_item_hot.unset_hot()
                        self.menu_item_hot = item
                        self.menu_item_hot_index = idx

    def reset(self):
        self.menu_item_hot_index = 0
        if self.menu_item_hot:
            self.menu_item_hot.unset_hot()
        self.menu_item_hot = self.menu_items[self.menu_item_hot_index]
        self.menu_item_hot.set_hot()
    
    def draw(self):
        for item in self.menu_items:
            self.screen.blit(item.rendered_text, (item.x, item.y))