#!/usr/bin/env python
from collections.abc import Callable
from pathlib import Path
from typing import Self

from aoc.utils import day_parser


class Day04:
    def __init__(self: Self, input_path: str):
        self.start, self.stop = self.parse_input(input_path)

    def parse_input(self: Self, input_path: str) -> tuple[int, int]:
        with Path(input_path).open() as in_file:
            start, stop = map(int, in_file.read().split("-"))

        return start, stop

    def criteria_match(
        self: Self, password: str, match_func: Callable[[int], bool]
    ) -> bool:
        if any(password[i] > password[i + 1] for i in range(len(password) - 1)):
            return False
        groups = [password.count(ch) for ch in set(password)]

        return any(match_func(group) for group in groups)


class TestMain:
    def test_part1(self: Self) -> None:
        ...
        # test = Day04(f"{Path(__file__).parent}/test_input_part1.txt")

    def test_part2(self: Self) -> None:
        ...
        # test = Day04(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day04(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(
            sum(
                solution.criteria_match(str(pass_num), lambda x: x >= 2)
                for pass_num in range(solution.start, solution.stop + 1)
            )
        )
    elif args.part == 2:
        print(
            sum(
                solution.criteria_match(str(pass_num), lambda x: x == 2)
                for pass_num in range(solution.start, solution.stop + 1)
            )
        )
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
