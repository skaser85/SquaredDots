from math import sqrt
import pygame
from dataclasses import dataclass
from Menu import Color
from colors import Colors

@dataclass
class Dot:
    index: int
    row: int
    col: int
    pos: pygame.Vector2
    size: int = 10
    color: pygame.Color = Colors.CYAN
    stroke_width: int = 1
    rect: pygame.Rect = None
    hovered: bool = False
    hovered_color: pygame.Color = Colors.MAGENTA
    selected: bool = False
    anim_duration: int = 255
    anim_timer: int = 255
    anim_speed: int = 10
    anim_start_color: pygame.Color = Colors.GREEN
    anim_target_color: pygame.Color = Colors.PURPLE
    available: bool = False

    def __post_init__(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

    def draw(self, screen: pygame.surface):
        if self.hovered and not self.selected:
            pygame.draw.ellipse(screen, self.hovered_color, self.rect, 0)
        elif self.selected:
            self.anim_timer -= self.anim_speed
            self.anim_timer = max(self.anim_timer, 0)
            if self.anim_timer == 0:
                self.anim_timer = self.anim_duration
                temp = Colors.copy(self.anim_start_color)
                self.anim_start_color = Colors.copy(self.anim_target_color)
                self.anim_target_color = temp
            lerp_amt = self.anim_timer / self.anim_duration
            c = Colors.copy(self.anim_start_color).lerp(self.anim_target_color, lerp_amt)
            pygame.draw.ellipse(screen, c, self.rect, 0)
        elif self.available and not self.selected:
            pygame.draw.ellipse(screen, Colors.PINK, self.rect, 0)
        pygame.draw.ellipse(screen, self.color, self.rect, self.stroke_width)

    def update(self, m: pygame.Vector2):
        self.hovered = self._mouse_is_over(m)

    def _mouse_is_over(self, m: pygame.Vector2):
        pos = pygame.Vector2(self.rect.center[0], self.rect.center[1])
        d = sqrt(pos.distance_squared_to(m))
        return d < self.size/2

    def _clamp(self, val, minimum, maximum):
        return max(minimum, min(val, maximum))