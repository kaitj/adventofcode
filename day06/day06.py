#!/usr/bin/env python
import re
from math import prod
from pathlib import Path

import pytest

from aoc.utils import day_parser


class Day06:
    def __init__(self, input: str, part_two: bool = False):
        self.races = self.load_race_info(input, part_two)

    def _extract_numbers(self, line: str, part_two: bool) -> list[int | str]:
        return [
            int(num.group()) if not part_two else num.group()
            for num in re.finditer(r"\d+", line)
        ]

    def load_race_info(self, input: str, part_two: bool) -> dict[str, list[int]]:
        with Path(input).open(encoding="utf-8") as in_file:
            regex = re.compile(r"[a-zA-Z]+")
            race_info: dict[str, list[int]] = (
                {
                    regex.match(line).group(): [  # pyright: ignore
                        int(
                            "".join(  # pyright: ignore
                                self._extract_numbers(line, part_two)  # pyright: ignore
                            )
                        )
                    ]
                    for line in in_file
                }
                if part_two
                else {
                    regex.match(line).group(): self._extract_numbers(  # pyright: ignore
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


class TestMain:
    @pytest.mark.parametrize(
        "time, distance, answer", [(7, 9, 4), (15, 40, 8), (30, 200, 9)]
    )
    def test_part1(self, time: int, distance: int, answer: int):
        test = Day06(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.num_finish(time=time, distance=distance) == answer
        assert prod(test.find_winning_ways()) == 288

    @pytest.mark.parametrize("key, answer", [("Time", 71530), ("Distance", 940200)])
    def test_part2(self, key: str, answer: int):
        test = Day06(f"{Path(__file__).parent}/test_input_part1.txt", part_two=True)
        assert test.races[key] == [answer]
        assert prod(test.find_winning_ways()) == 71503


def main():
    args = day_parser().parse_args()

    if args.part == 1:
        solution_p1 = Day06(f"{Path(__file__).parent}/input.txt")
        print(prod(solution_p1.find_winning_ways()))
    elif args.part == 2:
        solution_p2 = Day06(f"{Path(__file__).parent}/input.txt", part_two=True)
        print(prod(solution_p2.find_winning_ways()))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
