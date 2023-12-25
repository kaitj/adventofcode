#!/usr/bin/env python
"""
- calibration value = first + last digit
"""
import re
from pathlib import Path

from aoc.utils import day_parser

VALID_NUM = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}


class Day01:
    def __init__(self, input: str):
        self.lines = self.load_lines(input)

    def load_lines(self, input: str) -> list[str]:
        with open(input, encoding="utf-8") as in_file:
            return [line.strip("\n") for line in in_file]

    def get_calibration_value(self, part_two: bool) -> list[int]:
        calibration_values: list[int] = []

        for line in self.lines:
            if part_two:
                line = self.replace_valid_numbers(line)

            numbers = re.findall(r"\d", line)
            calibration_values.append(int(f"{numbers[0]}{numbers[-1]}"))

        return calibration_values

    def replace_valid_numbers(self, line: str) -> str:
        for word, replacement in VALID_NUM.items():
            line = line.replace(word, replacement)
        return line

    def sum_calibration_value(self, part_two: bool = False) -> int:
        return sum(self.get_calibration_value(part_two=part_two))


class TestMain:
    def test_part1(self):
        test = Day01(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.sum_calibration_value() == 142

    def test_part2(self):
        test = Day01(f"{Path(__file__).parent}/test_input_part2.txt")
        assert test.sum_calibration_value(part_two=True) == 281


def main():
    args = day_parser().parse_args()

    solution = Day01(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(solution.sum_calibration_value())
    elif args.part == 2:
        print(solution.sum_calibration_value(part_two=True))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
