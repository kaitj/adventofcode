#!/usr/bin/env python
from pathlib import Path
from typing import Self

from aoc.utils import day_parser


class Day00:
    def __init__(self: Self, input_path: str):
        ...


class TestMain:
    def test_part1(self: Self) -> None:
        ...
        # test = Day00(f"{Path(__file__).parent}/test_input_part1.txt")

    def test_part2(self: Self) -> None:
        ...
        # test = Day00(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day00(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        ...
    elif args.part == 2:
        ...
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
