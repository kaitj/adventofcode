#!/usr/bin/env python
import itertools as itx
import re
from collections import defaultdict
from math import prod
from pathlib import Path


class Number:
    def __init__(self, value: int, row: int, span: tuple[int, int]):
        self.value = value
        self.neighbors = self.find_neighbors(row=row, span=span)

    def find_neighbors(self, row: int, span: tuple[int, int]) -> set[tuple[int, int]]:
        return {
            (row + dx, col + dy)
            for dx, dy in itx.product((-1, 0, 1), (-1, 0, 1))
            for col in range(*span)
        }


class Day03:
    def __init__(self, input: str):
        self.lines = self.load_file(input)

    def load_file(self, input: str) -> list[str]:
        with Path(input).open(encoding="utf-8") as in_file:
            return [line.strip() for line in in_file]

    def find_nums(self) -> list[Number]:
        return [
            Number(value=int(num.group()), row=row, span=num.span())
            for row, line in enumerate(self.lines)
            for num in re.finditer(r"\d+", line)
        ]

    def find_symbols(self) -> set[tuple[int, int]]:
        return {
            (row, symbol.start())
            for row, line in enumerate(self.lines)
            for symbol in re.finditer(r"[^\.\w\s]", line)
        }

    def find_gear_part(
        self, part_two: bool = False
    ) -> list[int] | defaultdict[tuple[int, int], list[int]]:
        nums, symbols = self.find_nums(), self.find_symbols()

        if not part_two:
            return [num.value for num in nums if symbols & set(num.neighbors)]
        else:
            parts_by_symbol: dict[tuple[int, int], list[int]] = defaultdict(list)
            for symbol in symbols:
                for num in nums:
                    if symbol in num.neighbors:
                        parts_by_symbol[symbol].append(num.value)

            return parts_by_symbol


class TestMain:
    def test_part1(self):
        test = Day03(f"{Path(__file__).parent}/test_input_part1.txt")
        assert sum(test.find_gear_part()) == 4361  # pyright: ignore

    def test_part2(self):
        test = Day03(f"{Path(__file__).parent}/test_input_part2.txt")
        assert (
            sum(
                prod(val)  # pyright: ignore
                for val in test.find_gear_part(  # pyright: ignore
                    part_two=True
                ).values()  # pyright: ignore
                if len(val) == 2  # pyright: ignore
            )
            == 467835
        )


if __name__ == "__main__":
    solution = Day03(f"{Path(__file__).parent}/input.txt")
    print(sum(solution.find_gear_part()))  # pyright: ignore
    print(
        sum(
            prod(val)  # pyright: ignore
            for val in (  # pyright: ignore
                solution.find_gear_part(part_two=True)
            ).values()  # pyright: ignore
            if len(val) == 2  # pyright: ignore
        )
    )
