from __future__ import annotations
from dataclasses import dataclass
import math

def clamp(val: float, minimum: float, maximum: float):
    return max(minimum, min(val, maximum))

@dataclass
class Vec2:
    x: int = 0
    y: int = 0

    def add(self, v: Vec2) -> None:
        self.x += v.x
        self.y += v.y

    def sub(self, v: Vec2) -> None:
        self.x -= v.x
        self.y -= v.y

    def scale(self, s: int|float) -> None:
        self.x *= s
        self.y *= s

    def copy(self) -> Vec2:
        return Vec2(self.x, self.y)
    
    def lerp(self, v2: Vec2, t: float) -> None:
        self.x += (v2.x - self.x) * t
        self.y += (v2.y - self.y) * t

    def mag_sq(self):
        """
        Returns the sum of the squares of each component:
        x*x + y*y
        """
        return self.x * self.x + self.y * self.y

    def mag(self):
        """
        Returns the magnitude (length) of the vector.
        """
        return math.sqrt(self.mag_sq())

    @staticmethod
    def _add(v1: Vec2, v2: Vec2) -> Vec2:
        v = Vec2(v1.x, v1.y)
        v.x += v2.x
        v.y += v2.y
        return v

    @staticmethod
    def _sub(v1: Vec2, v2: Vec2) -> Vec2:
        v = Vec2(v1.x, v1.y)
        v.x -= v2.x
        v.y -= v2.y
        return v

    @staticmethod
    def _scale(v1: Vec2, s: int|float) -> Vec2:
        v = Vec2.copy(v1)
        v.x *= s
        v.y *= s
        return v

    @staticmethod
    def _copy(v: Vec2) -> Vec2:
        return Vec2(v.x, v.y)

    @staticmethod
    def _lerp(v1: Vec2, v2: Vec2, t: float) -> Vec2:
        v = Vec2.copy(v1)
        v.x += (v2.x - v1.x) * t
        v.y += (v2.y - v1.y) * t
        return v

    @staticmethod
    def _dist(v1: Vec2, v2: Vec2) -> float:
        """
        Returns the distance between the passed-in vectors
        """
        r = Vec2._copy(v1)
        r.sub(v2)
        return r.mag()

if __name__ == '__main__':
    v1 = Vec2(1,1)
    print(v1)
    v1.lerp(Vec2(10, 10), .25)
    print(v1)