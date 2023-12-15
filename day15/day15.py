#!/usr/bin/env python
import re
from collections import defaultdict
from pathlib import Path

import pytest

from aoc.utils import day_parser


class Day15:
    def __init__(self, input_path: str):
        self.steps = self.load_steps(input_path)

    def load_steps(self, input_path: str) -> list[str]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            steps = in_file.read().strip()

        return [step for step in steps.split(",")]

    def find_hash(self, step: str) -> int:
        hash = 0
        for ch in step:
            hash += ord(ch)
            hash *= 17
            hash %= 256

        return hash

    def find_hashmap(self) -> dict[int, list[str]]:
        hashmap: dict[int, list[str]] = defaultdict(list)

        for step in self.steps:
            label = re.match(r"\w+", step).group()  # pyright: ignore
            box = self.find_hash(label)
            found = [
                idx for idx, item in enumerate(hashmap[box]) if item.startswith(label)
            ]
            if "=" in step:
                if len(found) > 0:
                    hashmap[box][found[0]] = step.replace("=", " ")
                else:
                    hashmap[box].append(f"{step.replace("=", " ")}")
            else:
                if len(found) > 0:
                    hashmap[box].pop(found[0])

        return hashmap

    def focusing_power(self, hashmap: dict[int, list[str]]) -> list[int]:
        power: list[int] = [0 for _ in range(max(hashmap) + 1)]

        for box, lens in hashmap.items():
            # If no lens
            if len(lens) < 1:
                continue
            else:
                for slot, item in enumerate(lens, start=1):
                    value = int(re.search(r"\d+", item).group())  # pyright: ignore
                    power[box] += (box + 1) * slot * value

        return power


class TestMain:
    @pytest.mark.parametrize(
        "step, hash",
        [
            ("rn=1", 30),
            ("cm-", 253),
            ("qp=3", 97),
            ("cm=2", 47),
            ("qp-", 14),
            ("pc=4", 180),
        ],
    )
    def test_part1(self, step: str, hash: int) -> None:
        test = Day15(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.find_hash(step) == hash
        assert sum(test.find_hash(t_step) for t_step in test.steps) == 1320

    def test_part2(self) -> None:
        test = Day15(f"{Path(__file__).parent}/test_input_part1.txt")
        test_hashmap = test.find_hashmap()
        assert sum(test.focusing_power(test_hashmap)) == 145


def main():
    args = day_parser().parse_args()

    solution = Day15(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(sum(solution.find_hash(step) for step in solution.steps))
    elif args.part == 2:
        hashmap = solution.find_hashmap()
        print(sum(solution.focusing_power(hashmap)))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
