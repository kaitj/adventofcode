#!/usr/bin/env python
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from aoc.utils import day_parser


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self: Self) -> int:
        return hash((self.y, self.x))

    def __add__(self: Self, other: Self) -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def manhattan_dist(self: Self, other: Self) -> int | float:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Day03:
    def __init__(self: Self, input_path: str):
        self.start_pos = Position(x=0, y=0)
        self.wires = self.parse_input(input_path)

    def parse_input(self: Self, input_path: str) -> list[list[tuple[str, int]]]:
        with Path(input_path).open() as in_file:
            wires = [
                [(cmd[0], int(cmd[1:])) for cmd in line.split(",")] for line in in_file
            ]

        return wires

    def follow_wire(self: Self, wire: list[tuple[str, int]]) -> set[Position]:
        cur_pos = self.start_pos
        visited: set[Position] = set()

        for dir, steps in wire:
            if dir == "R":
                for _ in range(steps):
                    cur_pos = cur_pos + Position(x=1, y=0)
                    visited.add(cur_pos)
            elif dir == "L":
                for _ in range(steps):
                    cur_pos = cur_pos + Position(x=-1, y=0)
                    visited.add(cur_pos)
            elif dir == "U":
                for _ in range(steps):
                    cur_pos = cur_pos + Position(x=0, y=-1)
                    visited.add(cur_pos)
            elif dir == "D":
                for _ in range(steps):
                    cur_pos = cur_pos + Position(x=0, y=1)
                    visited.add(cur_pos)
            else:
                raise ValueError("Invalid direction")

        return visited

    def find_crossings(self: Self):
        all_visited = [self.follow_wire(wire) for wire in self.wires]

        if len(all_visited) != 2:
            raise ValueError("More than 2 wires were found")

        return all_visited[0] & all_visited[1]

    def min_manhattan_dist(self: Self, crossings: set[Position]) -> int | float:
        min_dist = float("inf")

        for crossing in crossings:
            min_dist = min(min_dist, self.start_pos.manhattan_dist(crossing))

        return min_dist


class TestMain:
    def test_part1(self: Self) -> None:
        test = Day03(f"{Path(__file__).parent}/test_input_part1.txt")
        test_crossings = test.find_crossings()
        assert test.min_manhattan_dist(test_crossings) == 6

    def test_part2(self: Self) -> None:
        ...
        # test = Day03(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day03(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        crossings = solution.find_crossings()
        print(solution.min_manhattan_dist(crossings))
    elif args.part == 2:
        ...
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
