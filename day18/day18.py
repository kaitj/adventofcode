#!/usr/bin/env python
from collections.abc import Generator
from math import inf
from pathlib import Path
from typing import Any


class Bounds:
    def __init__(self, cubes: set[tuple[int, int, int]]):
        mins = inf, inf, inf
        maxs = 0, 0, 0
        for cube in cubes:
            mins = tuple(map(min, zip(cube, mins)))  # type: ignore
            maxs = tuple(map(max, zip(cube, maxs)))  # type: ignore
        self.ranges = [set(range(lo - 1, hi + 2)) for lo, hi in zip(mins, maxs)]  # type: ignore
        self.mins = mins

    def __contains__(self, coords: tuple[int, ...]) -> bool:
        for cube, _range in zip(coords, self.ranges):
            if cube not in _range:
                return False
        return True


def parse_input(input_path: Path) -> set[tuple[int, int, int]]:
    with input_path.open(encoding="utf-8") as in_file:
        return set(tuple(map(int, line.strip().split(","))) for line in in_file)  # type: ignore


def neighbours(coords: tuple[int, ...]) -> Generator[tuple[int, ...], Any, Any]:
    x, y, z = coords
    for dx, dy, dz in (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ):
        yield x + dx, y + dy, z + dz


def solve_p1(cubes: set[tuple[int, ...]]) -> int:
    area = len(cubes) * 6
    for cube in cubes:
        for neighbour in neighbours(cube):
            area -= neighbour in cubes
    return area


def solve_p2(cubes: set[tuple[int, ...]]) -> int:
    bounds = Bounds(cubes)  # type: ignore
    q = [bounds.mins]
    seen = {bounds.mins}
    area = 0
    while q:
        coords = q.pop()
        for neighbour in neighbours(coords):  # type: ignore
            if neighbour in seen or neighbour not in bounds:  # type: ignore
                continue
            if neighbour in cubes:
                area += 1
            else:
                seen.add(neighbour)  # type: ignore
                q.append(neighbour)  # type: ignore

    return area


if __name__ == "__main__":
    in_file = Path(__file__).parent.joinpath("input.txt")
    cubes = parse_input(in_file)

    # Part 1
    print(f"Surface area of scanned lava droplet: {solve_p1(cubes)}")

    # Part 2
    print(f"Surface area of scanned lava droplet: {solve_p2(cubes)}")
