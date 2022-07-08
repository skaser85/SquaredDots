import pygame
from dataclasses import dataclass, field
from colors import Colors
from Dot import Dot

@dataclass
class Board:
    start_x: int
    start_y: int
    dots_x: int
    dots_y: int
    padding: int = 20
    dots: list = field(default_factory=list)
    hot_dot: Dot = None
    selected_dot: Dot = None

    def __post_init__(self):
        dx = self.start_x
        dy = self.start_y
        for y in range(self.dots_y):
            for x in range(self.dots_x):
                self.dots.append(Dot(pygame.Vector2(dx, dy)))
                dx += (self.padding + self.dots[0].size)
            dy += (self.padding + self.dots[0].size)
            dx = self.start_x

    def draw(self, surface: pygame.surface):
        for dot in self.dots:
            dot.draw(surface)

    def update(self, m: pygame.Vector2):
        self.hot_dot = None
        for dot in self.dots:
            dot.update(m)
            if dot.hovered:
                self.hot_dot = dot

    def handle_click(self):
        if self.hot_dot is None:
            return
        if self.selected_dot is None:
            self.selected_dot = self.hot_dot
            self.selected_dot.selected = True
        else:
            if self.selected_dot is not self.hot_dot:
                self.selected_dot.selected = False
                self.selected_dot = self.hot_dot
                self.selected_dot.selected = True
            else:
                self.selected_dot.selected = False
                self.selected_dot = None