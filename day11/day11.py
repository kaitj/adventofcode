#!/usr/bin/env python
import itertools as it
from copy import deepcopy
from pathlib import Path
from pprint import pformat
from unittest import TestCase

"""
- '.' = empty space
- '#' = galaxy
- rows and cols with no galaxies expand (e.g. 1 row -> 2 row)
- expand and then find shortest path between galaxies
"""

MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Day11:
    def __init__(self, input_path: str):
        self.orig_image = self.load_image(input_path)
        self.ORIG_ROWS = len(self.orig_image)
        self.ORIG_COLS = len(self.orig_image[0])

    def __repr__(self) -> str:
        return pformat(self.orig_image)

    def load_image(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            image = [[*line.strip()] for line in in_file]

        return image

    def find_empty_rows_cols(self) -> tuple[list[int], list[int]]:
        empty_rows: list[int] = []
        non_empty_cols: set[int] = set()

        for ridx, row in enumerate(self.orig_image):
            if "#" not in row:
                empty_rows.append(ridx)
            for cidx in (cols := range(self.ORIG_COLS)):
                if row[cidx] == "#":
                    non_empty_cols.add(cidx)

        return empty_rows, list(set(cols) ^ non_empty_cols)  # pyright: ignore

    def expand_universe(self) -> None:
        rows, cols = self.find_empty_rows_cols()
        expanded_image = deepcopy(self.orig_image)

        # Expand cols first
        for row in range(self.ORIG_ROWS):
            for cidx, col in enumerate(cols):
                expanded_image[row].insert(col + cidx, ".")
        # Expand rows
        for ridx, row in enumerate(rows):
            expanded_image.insert(row + ridx, ["."] * len(expanded_image[row]))

        self.image = expanded_image
        self.ROWS = len(expanded_image)
        self.COLS = len(expanded_image[0])

    def find_galaxies(self) -> None:
        self.galaxies: dict[int, tuple[int, int]] = {}
        galaxy = 0
        for ridx, row in enumerate(self.image):
            for cidx, col in enumerate(row):
                if col == "#":
                    galaxy += 1
                    self.galaxies[galaxy] = (ridx, cidx)

    def shortest_path(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def find_shortest_paths(self) -> list[int]:
        return [
            self.shortest_path(self.galaxies[g1], self.galaxies[g2])
            for g1, g2 in it.combinations(self.galaxies, 2)
        ]


class TestMain(TestCase):
    def test_part1(self):
        test = Day11(f"{Path(__file__).parent}/test_input_part1.txt")
        test.expand_universe()
        self.assertEqual(len(test.image), len(test.orig_image) + 2)
        self.assertEqual(len(test.image[0]), len(test.orig_image[0]) + 3)
        test.find_galaxies()
        self.assertEqual(
            test.shortest_path(start=test.galaxies[5], end=test.galaxies[9]), 9
        )
        self.assertEqual(
            test.shortest_path(start=test.galaxies[1], end=test.galaxies[7]), 15
        )
        self.assertEqual(
            test.shortest_path(start=test.galaxies[3], end=test.galaxies[6]), 17
        )
        self.assertEqual(
            test.shortest_path(start=test.galaxies[8], end=test.galaxies[9]), 5
        )
        self.assertEqual(sum(test.find_shortest_paths()), 374)

    def test_part2(self):
        raise NotImplementedError()
        test = Day11(f"{Path(__file__).parent}/test_input_part2.txt")


if __name__ == "__main__":
    solution = Day11(f"{Path(__file__).parent}/input.txt")
    solution.expand_universe()
    solution.find_galaxies()
    print(sum(solution.find_shortest_paths()))
