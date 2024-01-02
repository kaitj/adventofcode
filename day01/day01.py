#!/usr/bin/env python
from math import floor
from pathlib import Path
from typing import Self

import pytest

from aoc.utils import day_parser


class Day01:
    def __init__(self: Self, input_path: str | None):
        self.masses = self.parse_input(input_path) if input_path else None

    def parse_input(self: Self, input_path: str) -> list[int]:
        with Path(input_path).open() as in_file:
            masses = [int(line) for line in in_file]

        return masses

    def calc_fuel(self: Self, mass: int) -> int:
        return floor(mass / 3) - 2

    def fuel_requirements(self: Self, *, part_two: bool = False) -> int:
        fuels = [self.calc_fuel(mass) for mass in self.masses]  # type: ignore

        if part_two:
            for idx, fuel in enumerate(fuels):
                while fuel > 0:
                    fuel = self.calc_fuel(fuel)
                    if fuel <= 0:
                        break
                    fuels[idx] += fuel

        return sum(fuels)


class TestMain:
    @pytest.mark.parametrize(
        "mass, answer", [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
    )
    def test_part1(self: Self, mass: int, answer: int) -> None:
        test = Day01(None)
        assert test.calc_fuel(mass) == answer

    @pytest.mark.parametrize(
        "mass, answer", [(12, 2), (14, 2), (1969, 966), (100756, 50346)]
    )
    def test_part2(self: Self, mass: int, answer: int) -> None:
        test = Day01(None)
        test.masses = [mass]
        assert test.fuel_requirements(part_two=True) == answer


def main():
    args = day_parser().parse_args()

    solution = Day01(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(f"{solution.fuel_requirements()}")
    elif args.part == 2:
        print(f"{solution.fuel_requirements(part_two=True)}")
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
