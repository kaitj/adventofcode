#!/usr/bin/env python
from heapq import heappop, heappush
from pathlib import Path

from aoc.utils import day_parser

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Day17:
    def __init__(self, input_path: str):
        self.heat_map = self.load_map(input_path)
        self.rows = len(self.heat_map)
        self.cols = len(self.heat_map[0])

    def load_map(self, input_path: str) -> list[list[int]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            return [list(map(int, line.strip())) for line in in_file]

    def valid_move(self, cx: int, cy: int) -> bool:
        return 0 <= cx < self.cols and 0 <= cy < self.rows

    def find_neighbours(
        self,
        cur: tuple[int, int, tuple[int, int], int],
        min_moves: int,
        max_moves: int,
    ) -> list[tuple[int, int, tuple[int, int], int]]:
        """Find all valid neighbours, next direction and steps taken in current
        direction"""
        cx, cy, c_dir, steps = cur
        neighbours: list[tuple[int, int, tuple[int, int], int]] = []

        for dx, dy in DIRECTIONS:
            nx, ny = cx + dx, cy + dy

            if self.valid_move(nx, ny) and (-dx, -dy) != c_dir:
                new_steps = steps + 1 if (dx, dy) == c_dir else 1

                if new_steps > max_moves or (steps < min_moves and (dx, dy) != c_dir):
                    continue

                neighbours.append((nx, ny, (dx, dy), new_steps))

        return neighbours

    def find_path(self, min_moves: int = 0, max_moves: int = 3) -> int:
        cx, cy = 0, 0
        distances: dict[tuple[int, int, tuple[int, int], int], int] = {}
        q = []

        for dx, dy in [(1, 0), (0, 1)]:
            heappush(q, (0, (cx, cy, (dx, dy), 0)))  # pyright: ignore

        while q:
            (cost, cur) = heappop(q)  # pyright: ignore
            # If already visited
            if cur in distances:
                continue

            distances[cur] = cost  # pyright: ignore

            for neighbour in self.find_neighbours(
                cur,  # pyright: ignore
                min_moves,
                max_moves,
            ):
                if neighbour not in distances:  # pyright: ignore
                    new_cost = (  # pyright: ignore
                        cost + self.heat_map[neighbour[1]][neighbour[0]]
                    )
                    heappush(q, (new_cost, neighbour))  # pyright: ignore

        return min(
            [
                val
                for ((x, y, _, steps), val) in distances.items()
                if (x == self.cols - 1 and y == self.rows - 1) and steps >= min_moves
            ]
        )


class TestMain:
    def test_part1(self) -> None:
        test = Day17(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.find_path() == 102

    def test_part2(self) -> None:
        test = Day17(f"{Path(__file__).parent}/test_input_part2.txt")
        assert test.find_path(min_moves=4, max_moves=10) == 71


def main():
    args = day_parser().parse_args()

    solution = Day17(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(solution.find_path())
    elif args.part == 2:
        print(solution.find_path(min_moves=4, max_moves=10))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
