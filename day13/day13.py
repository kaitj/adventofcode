from dataclasses import dataclass

import utils


@dataclass
class Point:
    """Storing point data"""

    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


class Paper:
    """Paper containing dots"""

    def __init__(self, dots: set[Point]):
        self.__dots = dots

    def __repr__(self):
        """Output grid - replace . with ' ' for legibility"""
        grid = ""
        max_x = max(d.x for d in self.dots)
        max_y = max(d.y for d in self.dots)
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if Point(x, y) in self.dots:
                    grid += "#"
                else:
                    grid += " "
            grid += "\n"
        return grid

    @property
    def dots(self):
        return self.__dots

    def __fold_x(self, loc: int):
        """Fold across vertical line"""
        self.__dots = {
            Point(2 * loc - point.x, point.y) if point.x > loc else point
            for point in self.__dots
        }

    def __fold_y(self, loc: int):
        """Fold across horizontal line"""
        self.__dots = {
            Point(point.x, 2 * loc - point.y) if point.y > loc else point
            for point in self.__dots
        }

    def fold(self, axis: str, loc: int):
        match axis:
            case "x":
                self.__fold_x(loc)
            case "y":
                self.__fold_y(loc)
            case ValueError:
                raise ValueError(f"Invalid direction {axis}")


def puzzle(in_dots: list[str], in_instructions: list[str], fold_no: int):
    init_dots = {
        Point(int(x), int(y))
        for x, y, in (line.split(",") for line in in_dots.split("\n"))
    }

    paper = Paper(init_dots)

    for ins_no, instruction in enumerate(in_instructions.split("\n")):
        instruction = instruction.split("fold along ")[-1]
        axis, value = instruction.split("=")
        value = int(value)
        paper.fold(axis, value)
        if (ins_no + 1) == fold_no:
            return len(paper.dots)

    print(paper)


if __name__ == "__main__":
    in_fpath = input("Enter file path containing dots and instructions: ")
    dots, instructions = utils.parse_lines(in_fpath)

    # Puzzle 1
    print(f"The number of dot after one fold is: {puzzle(dots, instructions, 1)}")

    # Puzzle 2
    print(f"The secret code is: \n{puzzle(dots, instructions, None)}")
