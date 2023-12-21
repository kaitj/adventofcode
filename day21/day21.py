#!/usr/bin/env python
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from aoc.utils import day_parser


@dataclass
class Position:
    y: int
    x: int

    def __hash__(self):
        return hash((self.y, self.x))

    def __add__(self, other: "Position") -> "Position":
        return Position(y=self.y + other.y, x=self.x + other.x)


class Direction(Enum):
    Up = Position(y=-1, x=0)
    DOWN = Position(y=1, x=0)
    RIGHT = Position(y=0, x=1)
    LEFT = Position(y=0, x=-1)


class Day21:
    def __init__(self, input_path: str):
        self.map = self.load_map(input_path)

    def load_map(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            map: list[list[str]] = []
            for y, line in enumerate(in_file):
                if line.strip():
                    row: list[str] = []
                    for x, ch in enumerate(line.strip()):
                        if ch == "S":
                            self.start = Position(x=x, y=y)
                        row.append(ch)
                    map.append(row)
        return map

    def step(self, start_pos: Position) -> set[Position]:
        positions: set[Position] = set()
        for dir in Direction._member_map_.values():
            n_pos = start_pos + dir.value
            if self.map[n_pos.y][n_pos.x] != "#":
                positions.add(n_pos)
        return positions

    def process(self, start_pos: Position, steps: int = 1) -> set[Position]:
        positions = {start_pos}

        for _ in range(steps):
            n_position: set[Position] = set()
            for pos in positions:
                n_position = n_position.union(self.step(pos))
            positions = n_position  # type: ignore

        return positions


class TestMain:
    def test_part1(self) -> None:
        test = Day21(f"{Path(__file__).parent}/test_input_part1.txt")
        assert len(test.process(start_pos=test.start, steps=6)) == 16

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day21(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day21(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(len(solution.process(start_pos=solution.start, steps=64)))
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
