from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from _math import Vec2

@dataclass
class Mouse:
    pos: Vec2 = None
    left_down: bool = False
    right_down: bool = False
    middle_down: bool = False
    scrolled_up: bool = False
    scrolled_down: bool = False
    scrolled_amt_x: int = 0
    scrolled_amt_y: int = 0
    last_pos: Vec2 = None

    @staticmethod
    def next_frame(pm: Mouse = None) -> Mouse:
        m = Mouse()
        if pm:
            m.last_pos = pm.pos
        return m

    def set_pressed(self, pressed: Tuple[bool]) -> None:
        self.left_down = pressed[0]
        self.right_down = pressed[1]
        self.middle_down = pressed[2]
        self.scrolled_up = pressed[3]
        self.scrolled_down = pressed[4]

    def set_scroll(self, x: int, y: int) -> None:
        self.scrolled_amt_x = x
        self.scrolled_amt_y = y