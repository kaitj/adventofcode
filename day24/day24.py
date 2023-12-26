#!/usr/bin/env python
from collections import deque
from pathlib import Path
from typing import Literal, Self


class Blizzards:
    def __init__(self: Self, grid: list[str]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def traversable(self: Self, state: tuple[int, ...]) -> bool:
        r, c, t = state
        return (
            0 <= r < self.rows
            and 0 <= c < self.cols
            and self.grid[(r + t) % self.rows][c] != "^"
            and self.grid[(r - t) % self.rows][c] != "v"
            and self.grid[r][(c + t) % self.cols] != "<"
            and self.grid[r][(c - t) % self.cols] != ">"
        )


def parse_input(
    in_path: Path,
) -> tuple[Blizzards, tuple[Literal[0], Literal[0]], tuple[int, int]]:
    with in_path.open() as in_file:
        content = in_file.read()

    grid = [line[1:-1] for line in content.splitlines()[1:-1]]
    blizzards = Blizzards(grid)
    start = (0, 0)
    end = (blizzards.rows - 1, blizzards.cols - 1)

    return blizzards, start, end


def solve(
    blizzards: Blizzards, start: tuple[int, int], end: tuple[int, int], *, t: int = 0
) -> int:
    q = deque([(*start, t)])
    seen: set[tuple[int, ...]] = set()

    while True:
        r, c, t = q.popleft()

        if (r, c, t) in seen:
            continue
        if (r, c) == end:
            return t + 1

        seen.add((r, c, t))  # type: ignore

        for dr, dc in (-1, 0), (0, 1), (1, 0), (0, -1), (0, 0):
            state = r + dr, c + dc, t + 1
            if blizzards.traversable(state):
                q.append(state)
        if not q:
            q.append((*start, t + 1))


def solve_p2(blizzards: Blizzards, start: tuple[int, int], end: tuple[int, int]) -> int:
    split = solve(blizzards, start, end)
    split = solve(blizzards, end, start, t=split)

    return solve(blizzards, start, end, t=split)


if __name__ == "__main__":
    in_file = Path(__file__).parent.joinpath("input.txt")
    blizzards, start, end = parse_input(in_file)

    # Part 1
    print(f"Empty ground tiles: {solve(blizzards, start, end)}")

    # Part 2
    print(f"Fewest number of minutes: {solve_p2(blizzards, start, end)}")
