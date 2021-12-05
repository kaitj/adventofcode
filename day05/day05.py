from collections import defaultdict
from typing import Optional

import utils


class Point:
    """Point class containing (x,y) coordinates"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Line:
    """Line class containing start and end points"""

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    @classmethod
    def from_string(cls, line: str) -> "Line":
        point1, point2 = line.strip("\n").split(" -> ")
        x1, y1 = map(int, point1.split(","))
        x2, y2 = map(int, point2.split(","))

        return cls(Point(x1, y1), Point(x2, y2))


class Grid:
    """Grid class containing counts and lines"""

    def __init__(self, points: Optional[defaultdict[Point, int]] = None):
        self.points: defaultdict[Point, int] = points if points else defaultdict(int)

    def add_point(self, point: Point):
        """Increment counter"""
        self.points[point] += 1

    def add_line(self, line: Line, diag: bool = False):
        """Add line to grid"""
        # Horizontal line
        if line.start.y == line.end.y:
            start, end = min(line.start.x, line.end.x), max(line.start.x, line.end.x)
            for x in range(start, end + 1):
                self.add_point(Point(x, line.start.y))

        # Vertical line
        elif line.start.x == line.end.x:
            start, end = min(line.start.y, line.end.y), max(line.start.y, line.end.y)
            for y in range(start, end + 1):
                self.add_point(Point(line.start.x, y))

        # Diagonal line
        elif diag:
            x_dir = 1 if line.start.x < line.end.x else -1
            y_dir = 1 if line.start.y < line.end.y else -1
            x, y = line.start.x, line.start.y

            while not (x == line.end.x and y == line.end.y):
                self.add_point(Point(x, y))
                x += x_dir
                y += y_dir
            self.add_point(Point(x, y))

    def count_overlapping(self) -> int:
        """Count number of overlapping vents"""
        return sum(1 for _, count in self.points.items() if count >= 2)


def puzzle(in_coords, diag: bool = False):
    vent_grid = Grid()

    # Add lines
    for line in in_coords:
        line = Line.from_string(line)
        try:
            vent_grid.add_line(line, diag)
        except ValueError:
            pass

    # Count overlap
    return vent_grid.count_overlapping()


if __name__ == "__main__":
    data_fpath = input("Enter the filepath containing the location of vents: ")
    vent_coords = utils.parse_lines(data_fpath, str)

    print(f"Number of overlapping points: {puzzle(vent_coords)}")

    print(
        f"Number of overlapping vents including diagonals: {puzzle(vent_coords, True)}"
    )
