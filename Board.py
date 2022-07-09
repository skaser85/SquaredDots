from typing import List, Tuple, Union
import pygame
from dataclasses import dataclass, field
from enum import Enum, auto
from colors import Colors
from Dot import Dot
from Edge import Edge, Direction
from Square import Square

class Sides(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()

@dataclass
class Board:
    start_x: int
    start_y: int
    dots_x: int
    dots_y: int
    padding: int = 20
    dots: List[Dot] = field(default_factory=list)
    hot_dot: Dot = None
    selected_dot: Dot = None
    available_dots: List[Dot] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    squares: List[Square] = field(default_factory=list)

    def __post_init__(self):
        dx = self.start_x
        dy = self.start_y
        index = 0
        for r in range(self.dots_y):
            for c in range(self.dots_x):
                self.dots.append(Dot(index, r, c, pygame.Vector2(dx, dy)))
                index += 1
                dx += (self.padding + self.dots[0].size)
            dy += (self.padding + self.dots[0].size)
            dx = self.start_x

    def draw(self, surface: pygame.surface):
        for dot in self.dots:
            dot.draw(surface)
        for edge in self.edges:
            edge.draw(surface)
        for square in self.squares:
            square.draw(surface)

    def update(self, m: pygame.Vector2):
        self.hot_dot = None
        for dot in self.dots:
            dot.update(m)
            if dot.hovered:
                self.hot_dot = dot

    def handle_click(self):
        self.test_edges_down = []
        self.test_edges_up = []
        if self.hot_dot is None:
            if self.selected_dot is not None:
                self.selected_dot.selected = False
                self.selected_dot = None
                self.set_available()
            return
        
        if self.selected_dot is None:
            self.selected_dot = self.hot_dot
            self.selected_dot.selected = True
        else:
            if self.selected_dot is not self.hot_dot:
                if self.hot_dot in self.available_dots:
                    edge = Edge(self.selected_dot, self.hot_dot)
                    if self.edge_is_unique(edge):
                        if edge.direction == Direction.HORIZONTAL:
                            if edge.dot0.col > edge.dot1.col:
                                edge = Edge(edge.dot1, edge.dot0)
                        else:
                            if edge.dot0.row > edge.dot1.row:
                                edge = Edge(edge.dot1, edge.dot0)
                        
                        self.edges.append(edge)
                        
                        if edge.direction == Direction.HORIZONTAL:
                            if edge.dot0.row > 0:
                                success, s = self.check_for_square(edge, Sides.BOTTOM)
                                if success:
                                    self.squares.append(s)
                            if edge.dot0.row < (self.dots_y - 1):
                                success, s = self.check_for_square(edge, Sides.TOP)
                                if success:
                                    self.squares.append(s)
                        else:
                            if edge.dot0.col > 0:
                                success, s = self.check_for_square(edge, Sides.RIGHT)
                                if success:
                                    self.squares.append(s)
                            if edge.dot0.col < (self.dots_y - 1):
                                success, s = self.check_for_square(edge, Sides.LEFT)
                                if success:
                                    self.squares.append(s)
                    self.selected_dot.selected = False
                    self.selected_dot = self.hot_dot
                    self.selected_dot.selected = True
                else:
                    self.selected_dot.selected = False
                    self.selected_dot = self.hot_dot
                    self.selected_dot.selected = True
            else:
                self.selected_dot.selected = False
                self.selected_dot = None
        
        self.set_available()
    
    def set_available(self):
        if self.selected_dot is None:
            if len(self.available_dots) > 0:
                for dot in self.available_dots:
                    dot.available = False
        else:
            for dot in self.available_dots:
                dot.available = False
            self.available_dots = []
            r, c = self.get_row_col_from_index(self.selected_dot.index, self.dots_x)
            index = self.selected_dot.index
            if c > 0:
                dot = self.dots[self.get_index_from_row_col(r, c - 1, self.dots_x)]
                dot.available = True
                self.available_dots.append(dot)
            if c < (self.dots_x - 1):
                dot = self.dots[self.get_index_from_row_col(r, c + 1, self.dots_x)]
                dot.available = True
                self.available_dots.append(dot)
            if r > 0:
                dot = self.dots[self.get_index_from_row_col(r - 1, c, self.dots_x)]
                dot.available = True
                self.available_dots.append(dot)
            if r < (self.dots_y - 1):
                dot = self.dots[self.get_index_from_row_col(r + 1, c, self.dots_x)]
                dot.available = True
                self.available_dots.append(dot)
    
    def edge_is_unique(self, edge: Edge) -> bool:
        if len(self.edges) == 0:
            return True
        for e in self.edges:
            if (edge.dot0 == e.dot0 and edge.dot1 == e.dot1) or (edge.dot0 == e.dot1 and edge.dot1 == e.dot0):
                return False
        return True

    def all_edges_exist(self, t: Edge, tr: Edge, r: Edge, rr: Edge, b: Edge, br: Edge, l: Edge, lr: Edge) -> bool:
        return (t in self.edges or tr in self.edges) and\
               (r in self.edges or rr in self.edges) and\
               (b in self.edges or br in self.edges) and\
               (l in self.edges or lr in self.edges)

    def check_for_square(self, edge: Edge, side: Sides) -> Tuple[bool, Square]:
        if side in [Sides.TOP, Sides.BOTTOM]:
            if side == Sides.BOTTOM:
                e_bottom = edge
                e_bottom_rev = Edge(edge.dot1, edge.dot0)
                e_top, e_top_rev = self.make_side_edge(edge, Sides.TOP)
            else:
                e_top = edge
                e_top_rev = Edge(edge.dot1, edge.dot0)
                e_bottom, e_bottom_rev = self.make_side_edge(edge, Sides.BOTTOM)
            e_left = Edge(e_top.dot0, e_bottom.dot0)
            e_left_rev = Edge(e_bottom.dot0, e_top.dot0)            
            e_right = Edge(e_top.dot1, e_bottom.dot1)
            e_right_rev = Edge(e_bottom.dot1, e_top.dot1)
        if side in [Sides.RIGHT, Sides.LEFT]:
            if side == Sides.RIGHT:
                e_right = edge
                e_right_rev = Edge(edge.dot1, edge.dot0)
                e_left, e_left_rev = self.make_side_edge(edge, Sides.LEFT)
            else:
                e_left = edge
                e_left_rev = Edge(edge.dot1, edge.dot0)
                e_right, e_right_rev = self.make_side_edge(edge, Sides.RIGHT)
            e_top = Edge(e_left.dot0, e_right.dot0)
            e_top_rev = Edge(e_right.dot0, e_left.dot0)
            e_bottom = Edge(e_left.dot1, e_right.dot1)
            e_bottom_rev = Edge(e_right.dot1, e_left.dot1)

        success = self.all_edges_exist(e_top, e_top_rev, e_right, e_right_rev, e_bottom, e_bottom_rev, e_left, e_left_rev)
        s = None
        if success:
            s = Square(e_top, e_right, e_bottom, e_left, self.padding)
        
        return success, s

    def make_side_edge(self, edge: Edge, desired_side: Sides) -> Tuple[Edge]:
        if desired_side == Sides.TOP:
            dot0 = self.dots[self.get_index_from_row_col(edge.dot0.row - 1, edge.dot0.col, self.dots_x)]
            dot1 = self.dots[self.get_index_from_row_col(edge.dot1.row - 1, edge.dot1.col, self.dots_x)]
        elif desired_side == Sides.BOTTOM:
            dot0 = self.dots[self.get_index_from_row_col(edge.dot0.row + 1, edge.dot0.col, self.dots_x)]
            dot1 = self.dots[self.get_index_from_row_col(edge.dot1.row + 1, edge.dot1.col, self.dots_x)]
        elif desired_side == Sides.RIGHT:
            dot0 = self.dots[self.get_index_from_row_col(edge.dot0.row, edge.dot0.col + 1, self.dots_x)]
            dot1 = self.dots[self.get_index_from_row_col(edge.dot1.row, edge.dot1.col + 1, self.dots_x)]
        elif desired_side == Sides.LEFT:
            dot0 = self.dots[self.get_index_from_row_col(edge.dot0.row, edge.dot0.col - 1, self.dots_x)]
            dot1 = self.dots[self.get_index_from_row_col(edge.dot1.row, edge.dot1.col - 1, self.dots_x)]
        return (Edge(dot0, dot1), Edge(dot1, dot0))

    @staticmethod
    def get_row_col_from_index(index: int, width: int) -> Tuple[int]:
        return (index // width, index % width)

    @staticmethod
    def get_index_from_row_col(row: int, col: int, width: int) -> int:
        return (row * width) + col