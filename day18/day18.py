#!/usr/bin/env python
from dataclasses import dataclass
from pathlib import Path

from aoc.utils import day_parser


@dataclass
class Position:
    y: int
    x: int

    def __add__(self, other: "Position") -> "Position":
        return Position(y=self.y + other.y, x=self.x + other.x)

    def __mul__(self, other: int) -> "Position":
        return Position(y=self.y * other, x=self.x * other)


DIRECTIONS = {
    "U": Position(-1, 0),
    "D": Position(1, 0),
    "R": Position(0, 1),
    "L": Position(0, -1),
}

DIR_ENCODE = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


class Day18:
    def __init__(self, input_path: str):
        self.plan = self.load_plan(input_path)

    def load_plan(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            return [(line.strip().split(" ")) for line in in_file]

    def find_boundary(self, part_two: bool = False) -> tuple[list[Position], int]:
        pos = Position(0, 0)
        boundary = [pos]
        perimeter = 0

        for ch_dir, moves, encoding in self.plan:
            direction = DIRECTIONS[ch_dir]
            if part_two:
                direction = DIRECTIONS[DIR_ENCODE[encoding[-2]]]
                moves = int(encoding[2:-2], base=16)
            pos += direction * int(moves)  # pyright: ignore
            boundary.append(pos)  # pyright: ignore
            perimeter += int(moves)

        return boundary, perimeter

    def shoelace(self, boundary: list[Position], perimeter: int) -> int:
        val = 0
        for idx in range(len(boundary) - 1):
            pos1, pos2 = boundary[idx], boundary[idx + 1]
            val += pos2.y * pos1.x - pos2.x * pos1.y
        return abs(val // 2)

    def picks_theorem(self, boundary: list[Position], perimeter: int) -> int:
        return (
            self.shoelace(boundary=boundary, perimeter=perimeter) + perimeter // 2 + 1
        )


class TestMain:
    def test_part1(self) -> None:
        test = Day18(f"{Path(__file__).parent}/test_input_part1.txt")
        test_bounds, test_perim = test.find_boundary()
        assert test.picks_theorem(boundary=test_bounds, perimeter=test_perim) == 62

    def test_part2(self) -> None:
        test = Day18(f"{Path(__file__).parent}/test_input_part1.txt")
        test_bounds, test_perim = test.find_boundary(part_two=True)
        assert (
            test.picks_theorem(boundary=test_bounds, perimeter=test_perim)
            == 952408144115
        )


def main():
    args = day_parser().parse_args()

    solution = Day18(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        bounds, perim = solution.find_boundary()
        print(solution.picks_theorem(boundary=bounds, perimeter=perim))
    elif args.part == 2:
        bounds, perim = solution.find_boundary(True)
        print(solution.picks_theorem(boundary=bounds, perimeter=perim))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
