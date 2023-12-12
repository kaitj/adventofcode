#!/usr/bin/env python
import itertools as it
from pathlib import Path

import pytest

"""
- '.' = empty space
- '#' = galaxy
- rows and cols with no galaxies expand (e.g. 1 row -> 2 row)
- expand and then find shortest path between galaxies
"""

MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Day11:
    def __init__(self, input_path: str):
        self.image = self.load_image(input_path)
        self.ROWS = len(self.image)
        self.COLS = len(self.image[0])

    def load_image(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            image = [[*line.strip()] for line in in_file]

        return image

    def find_empty_rows_cols(self) -> tuple[list[int], list[int]]:
        empty_rows: list[int] = []
        non_empty_cols: set[int] = set()

        for ridx, row in enumerate(self.image):
            if "#" not in row:
                empty_rows.append(ridx)
            for cidx in (cols := range(self.COLS)):
                if row[cidx] == "#":
                    non_empty_cols.add(cidx)

        return empty_rows, list(set(cols) ^ non_empty_cols)  # pyright: ignore

    def find_galaxies(self) -> None:
        self.galaxies: dict[tuple[int, int], tuple[int, int]] = {}
        galaxy = 0
        for ridx, row in enumerate(self.image):
            for cidx, col in enumerate(row):
                if col == "#":
                    galaxy += 1
                    self.galaxies[(ridx, cidx)] = (ridx, cidx)

    def update_galaxy(
        self,
        coord: tuple[int, int],
        empty_cols: list[int],
        empty_rows: list[int],
        factor: int,
    ) -> tuple[int, int]:
        y, x = coord

        no_rows = sum(y > row for row in empty_rows) * factor
        no_cols = sum(x > col for col in empty_cols) * factor

        return y + no_rows, x + no_cols  # pyright: ignore

    def expand(self, factor: int = 2) -> None:
        if factor <= 1:
            raise ValueError("Universe must expand (i.e. factor >= 1)")
        factor -= 1

        empty_rows, empty_cols = self.find_empty_rows_cols()

        for galaxy in self.galaxies:
            self.galaxies[galaxy] = self.update_galaxy(
                coord=galaxy,
                empty_cols=empty_cols,
                empty_rows=empty_rows,
                factor=factor,
            )

    def shortest_path(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def find_shortest_paths(self) -> list[int]:
        return [
            self.shortest_path(self.galaxies[g1], self.galaxies[g2])
            for g1, g2 in it.combinations(self.galaxies, 2)
        ]


class TestMain:
    @pytest.mark.parametrize(
        "g1, g2, answer", [(5, 9, 9), (1, 7, 15), (3, 6, 17), (8, 9, 5)]
    )
    def test_part1(self, g1: int, g2: int, answer: int):
        test = Day11(f"{Path(__file__).parent}/test_input_part1.txt")
        test.find_galaxies()
        test.expand()
        test_keys = [key for key in test.galaxies]
        assert (
            test.shortest_path(
                start=test.galaxies[test_keys[g1 - 1]],
                end=test.galaxies[test_keys[g2 - 1]],
            )
            == answer
        )
        assert sum(test.find_shortest_paths()) == 374

    @pytest.mark.parametrize("factor, answer", [(10, 1030), (100, 8410)])
    def test_part2(self, factor: int, answer: int):
        test = Day11(f"{Path(__file__).parent}/test_input_part1.txt")
        test.find_galaxies()
        test.expand(factor=factor)
        assert sum(test.find_shortest_paths()) == answer


if __name__ == "__main__":
    solution = Day11(f"{Path(__file__).parent}/input.txt")
    solution.find_galaxies()
    solution.expand()
    print(sum(solution.find_shortest_paths()))
    solution.expand(factor=1_000_000)
    print(sum(solution.find_shortest_paths()))
