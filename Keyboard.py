from dataclasses import dataclass, field
from typing import Any

from pygame.locals import (
    K_ESCAPE,
    K_BACKSPACE,
    K_SPACE,
    K_RETURN,
    K_KP_ENTER,
    K_TAB,
    K_LSHIFT,
    K_RSHIFT,
    K_LCTRL,
    K_RCTRL,
    K_LALT,
    K_RALT,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

@dataclass
class Arrow:
    up: bool = False
    right: bool = False
    down: bool = False
    left: bool = False

@dataclass
class Keyboard:
    key: Any = None
    alt: bool = False
    backspace: bool = False
    ctrl: bool = False
    enter: bool = False
    escape: bool = False
    shift: bool = False
    space: bool = False
    tab: bool = False
    arrow: Arrow = field(init=False)

    def __post_init__(self):
        self.arrow = Arrow()

    def update(self, key: Any, key_unicode: str) -> None:
        if key == K_BACKSPACE:
            self.backspace = True
        elif key in [K_LALT, K_RALT]:
            self.alt = True
        elif key in [K_LCTRL, K_RCTRL]:
            self.ctrl = True
        elif key in [K_LSHIFT, K_RSHIFT]:
            self.shift = True
        elif key in [K_KP_ENTER, K_RETURN]:
            self.enter = True
        elif key == K_SPACE:
            self.space = True
        elif key == K_ESCAPE:
            self.escape = True
        elif key == K_TAB:
            self.tab = True
        elif key == K_UP:
            self.arrow.up = True
        elif key == K_RIGHT:
            self.arrow.right = True
        elif key == K_DOWN:
            self.arrow.down = True
        elif key == K_LEFT:
            self.arrow.left = True
        else:
            self.key = key_unicode