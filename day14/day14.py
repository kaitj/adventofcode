#!/usr/bin/env python
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

    def tilt_north(self) -> None:
        for cidx in range(self.COLS):
            dy = 0
            for ridx in range(self.ROWS):
                ch = self.rocks[ridx][cidx]
                if ch == ".":
                    dy += 1
                elif ch == "#":
                    dy = 0
                elif ch == "O":
                    self.rocks[ridx][cidx] = "."
                    self.rocks[ridx - dy][cidx] = "O"

    def tilt_south(self) -> None:
        for cidx in range(self.COLS):
            dy = 0
            for ridx in range(self.ROWS - 1, -1, -1):
                ch = self.rocks[ridx][cidx]
                if ch == ".":
                    dy += 1
                elif ch == "#":
                    dy = 0
                elif ch == "O":
                    self.rocks[ridx][cidx] = "."
                    self.rocks[ridx + dy][cidx] = "O"

    def tilt_east(self) -> None:
        for ridx in range(self.ROWS):
            dx = 0
            for cidx in range(self.COLS - 1, -1, -1):
                ch = self.rocks[ridx][cidx]
                if ch == ".":
                    dx += 1
                elif ch == "#":
                    dx = 0
                elif ch == "O":
                    self.rocks[ridx][cidx] = "."
                    self.rocks[ridx][cidx + dx] = "O"

    def tilt_west(self) -> None:
        for ridx in range(self.ROWS):
            dx = 0
            for cidx in range(self.COLS):
                ch = self.rocks[ridx][cidx]
                if ch == ".":
                    dx += 1
                elif ch == "#":
                    dx = 0
                elif ch == "O":
                    self.rocks[ridx][cidx] = "."
                    self.rocks[ridx][cidx - dx] = "O"

    def count_load(self) -> list[int]:
        return [
            row.count("O") * (self.ROWS - ridx) for ridx, row in enumerate(self.rocks)
        ]

    def cycle_tilt_load(self) -> list[int]:
        target = 1_000_000_000
        seen = {}
        loads: list[list[int]] = []
        for cycle in range(target):
            self.tilt_north()
            self.tilt_west()
            self.tilt_south()
            self.tilt_east()

            loads.append(self.count_load())

            state = "".join("".join(row) for row in self.rocks)
            if state in seen:
                break

            seen[state] = cycle

        first_rep = seen[state]  # pyright: ignore
        repetition_len = cycle - first_rep  # pyright: ignore
        no_cycles = (  # pyright: ignore
            first_rep + (target - first_rep) % repetition_len - 1
        )

        return loads[no_cycles]  # pyright: ignore


class TestMain:
    def test_part1(self) -> None:
        test = Day14(f"{Path(__file__).parent}/test_input_part1.txt")
        test.tilt_north()
        assert sum(test.count_load()) == 136

    def test_part2(self) -> None:
        test = Day14(f"{Path(__file__).parent}/test_input_part1.txt")
        assert sum(test.cycle_tilt_load()) == 64


def main():
    args = day_parser().parse_args()

    solution = Day14(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        solution.tilt_north()
        print(sum(solution.count_load()))
    elif args.part == 2:
        print(sum(solution.cycle_tilt_load()))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
