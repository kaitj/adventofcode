#!/usr/bin/env python
from copy import deepcopy
from pathlib import Path

from aoc.utils import day_parser


class Day14:
    def __init__(self, input_path: str):
        self.rocks = self.load_rocks(input_path)
        self.ROWS = len(self.rocks)
        self.COLS = len(self.rocks[0])

    def load_rocks(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            rocks = [[*row.strip()] for row in in_file]

        return rocks

    def tilt(self) -> list[list[str]]:
        tilted_rocks = deepcopy(self.rocks)
        for cidx in range(self.COLS):
            dy = 0
            for ridx in range(self.ROWS):
                ch = tilted_rocks[ridx][cidx]
                if ch == ".":
                    dy += 1
                elif ch == "#":
                    dy = 0
                elif ch == "O":
                    tilted_rocks[ridx][cidx] = "."
                    tilted_rocks[ridx - dy][cidx] = "O"

        return tilted_rocks

    def count_load(self, tilted_rocks: list[list[str]]) -> list[int]:
        return [
            row.count("O") * (self.ROWS - ridx) for ridx, row in enumerate(tilted_rocks)
        ]


class TestMain:
    def test_part1(self) -> None:
        test = Day14(f"{Path(__file__).parent}/test_input_part1.txt")
        test_tilted_rocks = test.tilt()
        assert sum(test.count_load(test_tilted_rocks)) == 136

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day14(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day14(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        tilt_rocks = solution.tilt()
        print(sum(solution.count_load(tilt_rocks)))
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
