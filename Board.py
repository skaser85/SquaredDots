from typing import List, Tuple
import pygame
from dataclasses import dataclass, field
from colors import Colors
from Dot import Dot
from Edge import Edge, Direction
from Square import Square

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
                                e_bottom = edge
                                
                                dot0_up = self.dots[self.get_index_from_row_col(e_bottom.dot0.row - 1, e_bottom.dot0.col, self.dots_x)]
                                dot1_up = self.dots[self.get_index_from_row_col(e_bottom.dot1.row - 1, e_bottom.dot1.col, self.dots_x)]
                                
                                e_top = Edge(dot0_up, dot1_up)
                                e_top_rev = Edge(dot1_up, dot0_up)
                                
                                e_left = Edge(e_top.dot0, e_bottom.dot0)
                                e_left_rev = Edge(e_bottom.dot0, e_top.dot0)
                                
                                e_right = Edge(e_top.dot1, e_bottom.dot1)
                                e_right_rev = Edge(e_bottom.dot1, e_top.dot1)
                                
                                if (e_top in self.edges or e_top_rev in self.edges) and\
                                   (e_left in self.edges or e_left_rev in self.edges) and\
                                   (e_right in self.edges or e_right_rev in self.edges):
                                    s = Square(e_top, e_right, e_bottom, e_left, self.padding)
                                    self.squares.append(s)
                            if edge.dot0.row < (self.dots_y - 1):
                                e_top = edge
                                
                                dot0_down = self.dots[self.get_index_from_row_col(e_top.dot0.row + 1, e_top.dot0.col, self.dots_x)]
                                dot1_down = self.dots[self.get_index_from_row_col(e_top.dot1.row + 1, e_top.dot1.col, self.dots_x)]
                                
                                e_bottom = Edge(dot0_down, dot1_down)
                                e_bottom_rev = Edge(dot1_down, dot0_down)
                                
                                e_left = Edge(e_top.dot0, e_bottom.dot0)
                                e_left_rev = Edge(e_bottom.dot0, e_top.dot0)
                                
                                e_right = Edge(e_top.dot1, e_bottom.dot1)
                                e_right_rev = Edge(e_bottom.dot1, e_top.dot1)
                                
                                if (e_bottom in self.edges or e_bottom_rev in self.edges) and\
                                   (e_left in self.edges or e_left_rev in self.edges) and\
                                   (e_right in self.edges or e_right_rev in self.edges):
                                    s = Square(e_top, e_right, e_bottom, e_left, self.padding)
                                    self.squares.append(s)
                        else:
                            if edge.dot0.col > 0:
                                e_right = edge
                                
                                dot0_left = self.dots[self.get_index_from_row_col(e_right.dot0.row, e_right.dot0.col - 1, self.dots_x)]
                                dot1_left = self.dots[self.get_index_from_row_col(e_right.dot1.row, e_right.dot1.col - 1, self.dots_x)]
                                
                                e_left = Edge(dot0_left, dot1_left)
                                e_left_rev = Edge(dot1_left, dot0_left)
                                
                                e_top = Edge(e_left.dot0, e_right.dot0)
                                e_top_rev = Edge(e_right.dot0, e_left.dot0)

                                e_bottom = Edge(e_left.dot1, e_right.dot1)
                                e_bottom_rev = Edge(e_right.dot1, e_left.dot1)
                                
                                if (e_top in self.edges or e_top_rev in self.edges) and\
                                   (e_left in self.edges or e_left_rev in self.edges) and\
                                   (e_bottom in self.edges or e_bottom_rev in self.edges):
                                    s = Square(e_top, e_right, e_bottom, e_left, self.padding)
                                    self.squares.append(s)
                            if edge.dot0.col < (self.dots_y - 1):
                                e_left = edge
                                
                                dot0_right = self.dots[self.get_index_from_row_col(e_left.dot0.row, e_left.dot0.col + 1, self.dots_x)]
                                dot1_right = self.dots[self.get_index_from_row_col(e_left.dot1.row, e_left.dot1.col + 1, self.dots_x)]
                                
                                e_right = Edge(dot0_right, dot1_right)
                                e_right_rev = Edge(dot1_right, dot0_right)
                                
                                e_top = Edge(e_left.dot0, e_right.dot0)
                                e_top_rev = Edge(e_right.dot0, e_left.dot0)

                                e_bottom = Edge(e_left.dot1, e_right.dot1)
                                e_bottom_rev = Edge(e_right.dot1, e_left.dot1)
                                
                                if (e_top in self.edges or e_top_rev in self.edges) and\
                                   (e_right in self.edges or e_right_rev in self.edges) and\
                                   (e_bottom in self.edges or e_bottom_rev in self.edges):
                                    s = Square(e_top, e_right, e_bottom, e_left, self.padding)
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

    @staticmethod
    def get_row_col_from_index(index: int, width: int) -> Tuple[int]:
        return (index // width, index % width)

    @staticmethod
    def get_index_from_row_col(row: int, col: int, width: int) -> int:
        return (row * width) + col