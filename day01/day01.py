#!/usr/bin/env python
"""
- calibration value = first + last digit
"""
import re
from unittest import TestCase

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

    def load_lines(self, input: str):
        with open(input, "r", encoding="utf-8") as in_file:
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


class TestMain(TestCase):
    def test_part1(self):
        test = Day01("./day01/test_input_part1.txt")
        self.assertEqual(test.sum_calibration_value(), 142)

    def test_part2(self):
        test = Day01("./day01/test_input_part2.txt")
        self.assertEqual(test.sum_calibration_value(part_two=True), 281)


if __name__ == "__main__":
    solution = Day01("./day01/input.txt")
    print(solution.sum_calibration_value())
    print(solution.sum_calibration_value(part_two=True))
