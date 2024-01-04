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

    def follow_wire(
        self: Self, wire: list[tuple[str, int]], crossing: Position | None = None
    ) -> set[Position] | int:
        cur_pos = self.start_pos
        visited: set[Position] = set()
        step_counter = 0

        for dir, steps in wire:
            for _ in range(steps):
                if dir == "R":
                    cur_pos = cur_pos + Position(x=1, y=0)
                    visited.add(cur_pos)
                elif dir == "L":
                    cur_pos = cur_pos + Position(x=-1, y=0)
                    visited.add(cur_pos)
                elif dir == "U":
                    cur_pos = cur_pos + Position(x=0, y=-1)
                    visited.add(cur_pos)
                elif dir == "D":
                    cur_pos = cur_pos + Position(x=0, y=1)
                    visited.add(cur_pos)
                else:
                    raise ValueError("Invalid direction")

                step_counter += 1

                if cur_pos == crossing:
                    return step_counter

        return visited

    def find_crossings(self: Self) -> set[Position]:
        all_visited = [self.follow_wire(wire) for wire in self.wires]

        if len(all_visited) != 2:
            raise ValueError("More / less than 2 wires were found")

        return all_visited[0] & all_visited[1]  # type: ignore

    def min_manhattan_dist(self: Self, crossings: set[Position]) -> int | float:
        min_dist = float("inf")

        for crossing in crossings:
            min_dist = min(min_dist, self.start_pos.manhattan_dist(crossing))

        return min_dist

    def find_steps(self: Self, crossings: set[Position]) -> int:
        return min(
            [
                sum(self.follow_wire(wire, crossing) for wire in self.wires)  # type: ignore
                for crossing in crossings
            ]
        )


class TestMain:
    def test_part1(self: Self) -> None:
        test = Day03(f"{Path(__file__).parent}/test_input_part1.txt")
        test_crossings = test.find_crossings()
        assert test.min_manhattan_dist(test_crossings) == 6

    def test_part2(self: Self) -> None:
        test = Day03(f"{Path(__file__).parent}/test_input_part1.txt")
        test_crossing = test.find_crossings()
        assert test.find_steps(test_crossing) == 30


def main():
    args = day_parser().parse_args()

    solution = Day03(f"{Path(__file__).parent}/input.txt")
    crossings = solution.find_crossings()
    if args.part == 1:
        print(solution.min_manhattan_dist(crossings))
    elif args.part == 2:
        print(solution.find_steps(crossings))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
