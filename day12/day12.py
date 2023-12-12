#!/usr/bin/env python
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

import pytest


class Spring(NamedTuple):
    pattern: str
    condition: tuple[int, ...]


class Day12:
    def __init__(self, input_path: str, factor: int = 1):
        self.springs = self.load_springs(input_path, factor)

    def load_springs(self, input_path: str, factor: int) -> list[Spring]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            springs = [
                Spring(
                    pattern=line.split()[0]
                    if factor == 1
                    else ("".join((line.split()[0], "?")) * factor)[:-1],
                    condition=tuple(map(int, line.split()[1].strip().split(",")))
                    * factor,
                )
                for line in in_file
            ]

        return springs

    @lru_cache
    def calc_arrangements(self, pattern: str, condition: tuple[int, ...]) -> int:
        # If no more patterns, make sure no more conditions to check
        if not pattern:
            return len(condition) == 0

        # If no more conditions to check, make sure no more "damaged"
        if not condition:
            return "#" not in pattern

        arrangements = 0

        # If pattern is undamaged or unknown. check remaining pattern
        if pattern[0] in ".?":
            arrangements += self.calc_arrangements(pattern[1:], condition)

        # If pattern is damaged or unknown, check next block and remaining conditions
        if (
            pattern[0] in "#?"
            and condition[0] <= len(pattern)
            and "." not in pattern[: condition[0]]
            and (condition[0] == len(pattern) or pattern[condition[0]] != "#")
        ):
            arrangements += self.calc_arrangements(
                pattern[condition[0] + 1 :], condition[1:]
            )

        return arrangements

    def find_all_spring_arrangements(self) -> list[int]:
        arrangements = [
            self.calc_arrangements(pattern=spring.pattern, condition=spring.condition)
            for spring in self.springs
        ]

        return arrangements


class TestMain:
    @pytest.mark.parametrize(
        "spring, answer",
        [
            (0, 1),
            (1, 4),
            (2, 1),
            (3, 1),
            (4, 4),
            (5, 10),
        ],
    )
    def test_part1(self, spring: int, answer: int) -> None:
        test = Day12(f"{Path(__file__).parent}/test_input_part1.txt")
        assert (
            test.calc_arrangements(
                pattern=test.springs[spring].pattern,
                condition=test.springs[spring].condition,
            )
            == answer
        )
        assert sum(test.find_all_spring_arrangements()) == 21

    @pytest.mark.parametrize(
        "spring, answer",
        [
            (0, 1),
            (1, 16384),
            (2, 1),
            (3, 16),
            (4, 2500),
            (5, 506250),
        ],
    )
    def test_part2(self, spring: int, answer: int) -> None:
        test = Day12(f"{Path(__file__).parent}/test_input_part1.txt", factor=5)
        assert (
            test.calc_arrangements(
                pattern=test.springs[spring].pattern,
                condition=test.springs[spring].condition,
            )
            == answer
        )
        assert test.find_all_spring_arrangements()


if __name__ == "__main__":
    solution_p1 = Day12(f"{Path(__file__).parent}/input.txt")
    print(sum(solution_p1.find_all_spring_arrangements()))
    solution_p2 = Day12(f"{Path(__file__).parent}/input.txt", factor=5)
    print(sum(solution_p2.find_all_spring_arrangements()))
