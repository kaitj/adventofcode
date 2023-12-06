#!/usr/bin/env python
import re
from math import prod
from pathlib import Path
from unittest import TestCase


class Day06:
    def __init__(self, input: str, part_two: bool = False):
        self.races = self.load_race_info(input, part_two)

    def _extract_numbers(self, line: str, part_two: bool) -> list[int | str]:
        return [
            int(num.group()) if not part_two else num.group()
            for num in re.finditer(r"\d+", line)
        ]

    def load_race_info(
        self, input: str, part_two: bool
    ) -> dict[str, list[int]]:
        with Path(input).open(encoding="utf-8") as in_file:
            regex = re.compile(r"[a-zA-Z]+")
            race_info: dict[str, list[int]] = (
                {
                    regex.match(line).group(): [  # pyright: ignore
                        int(
                            "".join(  # pyright: ignore
                                self._extract_numbers(
                                    line, part_two
                                )  # pyright: ignore
                            )
                        )
                    ]
                    for line in in_file
                }
                if part_two
                else {
                    regex.match(
                        line
                    ).group(): self._extract_numbers(  # pyright: ignore
                        line, part_two
                    )
                    for line in in_file
                }
            )

        return race_info

    def find_winning_ways(self) -> list[int]:
        winning_ways: list[int] = [1]
        for time, distance in zip(self.races["Time"], self.races["Distance"]):
            winning_ways.append(self.num_finish(time, distance))

        return winning_ways

    def num_finish(self, time: int, distance: int) -> int:
        finish = 0
        for hold_time in range(time):
            if hold_time * (time - hold_time) > distance:
                finish += 1

        return finish


class TestMain(TestCase):
    def test_part1(self):
        test = Day06(f"{Path(__file__).parent}/test_input_part1.txt")
        self.assertEqual(test.num_finish(time=7, distance=9), 4)
        self.assertEqual(test.num_finish(time=15, distance=40), 8)
        self.assertEqual(test.num_finish(time=30, distance=200), 9)
        self.assertEqual(prod(test.find_winning_ways()), 288)

    def test_part2(self):
        test = Day06(
            f"{Path(__file__).parent}/test_input_part1.txt", part_two=True
        )
        self.assertEqual(test.races["Time"], [71530])
        self.assertEqual(test.races["Distance"], [940200])
        self.assertEqual(prod(test.find_winning_ways()), 71503)


if __name__ == "__main__":
    solution_p1 = Day06(f"{Path(__file__).parent}/input.txt")
    print(prod(solution_p1.find_winning_ways()))
    solution_p2 = Day06(f"{Path(__file__).parent}/input.txt", part_two=True)
    print(prod(solution_p2.find_winning_ways()))
