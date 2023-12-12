#!/usr/bin/env python
from pathlib import Path

from aoc.utils import day_parser


class Day00:
    def __init__(self, input_path: str):
        raise NotImplementedError()


class TestMain:
    def test_part1(self) -> None:
        raise NotImplementedError()
        # test = Day00(f"{Path(__file__).parent}/test_input_part1.txt")

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day00(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day00(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        raise NotImplementedError()
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
