from typing import List, Tuple
import pygame
from dataclasses import dataclass, field
from enum import Enum, auto
from Dot import Dot
from Edge import Edge, Direction
from Square import Square
from Player import Player
from colors import Colors, Color

class Sides(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()

@dataclass
class Board:
    start_x: int
    start_y: int
    max_x: int
    max_y: int
    font: pygame.font.Font
    color: Color
    dots_x: int = 0
    dots_y: int = 0
    padding: int = 20
    dots: List[Dot] = field(default_factory=list)
    hot_dot: Dot = None
    selected_dot: Dot = None
    available_dots: List[Dot] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    squares: List[Square] = field(default_factory=list)
    player: Player = None
    rect: pygame.Rect = None
    is_hot: bool = False

    def __post_init__(self):
        self.dots_x = 0
        while (self.start_x + (self.dots_x * Dot.size) + (self.dots_x * self.padding) - self.padding) <= self.max_x:
            self.dots_x += 1
        self.dots_y = 0
        while (self.start_y + (self.dots_y * Dot.size) + (self.dots_y * self.padding) - self.padding) <= self.max_y:
            self.dots_y += 1
        board_start_x = self.start_x - self.padding
        board_start_y = self.start_y - self.padding
        board_end_x = 0
        board_end_y = 0
        dx = self.start_x
        dy = self.start_y
        index = 0
        for r in range(self.dots_y):
            for c in range(self.dots_x):
                self.dots.append(Dot(index, r, c, pygame.Vector2(dx, dy)))
                index += 1
                dx += (self.padding + self.dots[0].size)
            dy += (self.padding + self.dots[0].size)
            if board_end_x == 0:
                board_end_x = dx
            dx = self.start_x
        board_end_y = dy
        self.rect = pygame.Rect(board_start_x, board_start_y, board_end_x - board_start_x, board_end_y - board_start_y)

    def draw(self, surface: pygame.surface):
        c = self.color
        if self.is_hot:
            c = c.brighten(c, 0.1)
        pygame.draw.rect(surface, c.color, self.rect)
        for dot in self.dots:
            dot.draw(surface)
        for edge in self.edges:
            edge.draw(surface)
        for square in self.squares:
            square.draw(surface)

    def update(self, m: pygame.Vector2):
        self.is_hot = self.rect.collidepoint(m.x, m.y)
        self.hot_dot = None
        for dot in self.dots:
            dot.update(m)
            if dot.hovered:
                self.hot_dot = dot

    def handle_click(self):
        self.test_edges_down = []
        self.test_edges_up = []
        squares_completed = 0
        move_made = False
        if self.hot_dot is None:
            if self.selected_dot is not None:
                self.selected_dot.selected = False
                self.selected_dot = None
                self.set_available()
            return move_made, squares_completed
        
        if self.selected_dot is None:
            self.selected_dot = self.hot_dot
            self.selected_dot.selected = True
            self.set_available()
        else:
            if self.selected_dot is not self.hot_dot:
                if self.hot_dot in self.available_dots:
                    edge = Edge(self.selected_dot, self.hot_dot, self.player.color)
                    if not self.edge_exists(edge):
                        move_made = True
                        if edge.direction == Direction.HORIZONTAL:
                            if edge.dot0.col > edge.dot1.col:
                                edge = Edge(edge.dot1, edge.dot0, self.player.color)
                        else:
                            if edge.dot0.row > edge.dot1.row:
                                edge = Edge(edge.dot1, edge.dot0, self.player.color)
                        
                        self.edges.append(edge)
                        
                        if edge.direction == Direction.HORIZONTAL:
                            if edge.dot0.row > 0:
                                success, s = self.check_for_square(edge, Sides.BOTTOM)
                                if success:
                                    squares_completed += 1
                                    self.squares.append(s)
                            if edge.dot0.row < (self.dots_y - 1):
                                success, s = self.check_for_square(edge, Sides.TOP)
                                if success:
                                    squares_completed += 1
                                    self.squares.append(s)
                        else:
                            if edge.dot0.col > 0:
                                success, s = self.check_for_square(edge, Sides.RIGHT)
                                if success:
                                    squares_completed += 1
                                    self.squares.append(s)
                            if edge.dot0.col < (self.dots_y - 1):
                                success, s = self.check_for_square(edge, Sides.LEFT)
                                if success:
                                    squares_completed += 1
                                    self.squares.append(s)
                    self.selected_dot.selected = False
                    self.selected_dot = self.hot_dot
                    self.selected_dot.selected = True
                    self.set_available()
                else:
                    self.selected_dot.selected = False
                    self.selected_dot = self.hot_dot
                    self.selected_dot.selected = True
                    self.set_available()
            else:
                self.selected_dot.selected = False
                self.selected_dot = None
                self.deselect_dot()

        return move_made, squares_completed

    def deselect_dot(self):
        if self.selected_dot:
            self.selected_dot.selected = False
            self.selected_dot = None

    def clear_available(self):
        for dot in self.available_dots:
            dot.available = False
        self.available_dots = []
    
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
            if c > 0:
                dot = self.dots[self.get_index_from_row_col(r, c - 1, self.dots_x)]
                self.add_to_available(dot)
            if c < (self.dots_x - 1):
                dot = self.dots[self.get_index_from_row_col(r, c + 1, self.dots_x)]
                self.add_to_available(dot)
            if r > 0:
                dot = self.dots[self.get_index_from_row_col(r - 1, c, self.dots_x)]
                self.add_to_available(dot)
            if r < (self.dots_y - 1):
                dot = self.dots[self.get_index_from_row_col(r + 1, c, self.dots_x)]
                self.add_to_available(dot)

    def add_to_available(self, dot: Dot) -> None:
        edge = Edge(self.selected_dot, dot, self.player.color)
        if not self.edge_exists(edge):
            dot.available = True
            self.available_dots.append(dot)
    
    def edge_exists(self, edge: Edge) -> bool:
        if len(self.edges) == 0:
            return False
        for e in self.edges:
            if (edge.dot0 == e.dot0 and edge.dot1 == e.dot1) or (edge.dot0 == e.dot1 and edge.dot1 == e.dot0):
                return True
        return False

    def all_edges_exist(self, t: Edge, r: Edge, b: Edge, l: Edge) -> bool:
        return (self.edge_exists(t) and self.edge_exists(r) and self.edge_exists(b) and self.edge_exists(l))

    def check_for_square(self, edge: Edge, side: Sides) -> Tuple[bool, Square]:
        if side in [Sides.TOP, Sides.BOTTOM]:
            if side == Sides.BOTTOM:
                e_bottom = edge
                e_top = self.make_side_edge(edge, Sides.TOP)
            else:
                e_top = edge
                e_bottom = self.make_side_edge(edge, Sides.BOTTOM)
            e_left = Edge(e_top.dot0, e_bottom.dot0, self.player.color)
            e_right = Edge(e_top.dot1, e_bottom.dot1, self.player.color)
        if side in [Sides.RIGHT, Sides.LEFT]:
            if side == Sides.RIGHT:
                e_right = edge
                e_left = self.make_side_edge(edge, Sides.LEFT)
            else:
                e_left = edge
                e_right = self.make_side_edge(edge, Sides.RIGHT)
            e_top = Edge(e_left.dot0, e_right.dot0, self.player.color)
            e_bottom = Edge(e_left.dot1, e_right.dot1, self.player.color)

        success = self.all_edges_exist(e_top, e_right, e_bottom, e_left)
        s = None
        if success:
            s = Square(e_top, e_right, e_bottom, e_left, self.padding, self.player, self.font)
        
        return success, s

    def make_side_edge(self, opposite_edge: Edge, desired_side: Sides) -> Edge:
        if desired_side == Sides.TOP:
            dot0 = self.dots[self.get_index_from_row_col(opposite_edge.dot0.row - 1, opposite_edge.dot0.col, self.dots_x)]
            dot1 = self.dots[self.get_index_from_row_col(opposite_edge.dot1.row - 1, opposite_edge.dot1.col, self.dots_x)]
        elif desired_side == Sides.BOTTOM:
            dot0 = self.dots[self.get_index_from_row_col(opposite_edge.dot0.row + 1, opposite_edge.dot0.col, self.dots_x)]
            dot1 = self.dots[self.get_index_from_row_col(opposite_edge.dot1.row + 1, opposite_edge.dot1.col, self.dots_x)]
        elif desired_side == Sides.RIGHT:
            dot0 = self.dots[self.get_index_from_row_col(opposite_edge.dot0.row, opposite_edge.dot0.col + 1, self.dots_x)]
            dot1 = self.dots[self.get_index_from_row_col(opposite_edge.dot1.row, opposite_edge.dot1.col + 1, self.dots_x)]
        elif desired_side == Sides.LEFT:
            dot0 = self.dots[self.get_index_from_row_col(opposite_edge.dot0.row, opposite_edge.dot0.col - 1, self.dots_x)]
            dot1 = self.dots[self.get_index_from_row_col(opposite_edge.dot1.row, opposite_edge.dot1.col - 1, self.dots_x)]
        return Edge(dot0, dot1, self.player.color)

    def set_player(self, player: Player) -> None:
        self.player = player

    @staticmethod
    def get_row_col_from_index(index: int, width: int) -> Tuple[int]:
        return (index // width, index % width)

    @staticmethod
    def get_index_from_row_col(row: int, col: int, width: int) -> int:
        return (row * width) + col