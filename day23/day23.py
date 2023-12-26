#!/usr/bin/env python
import itertools as it
import operator as op
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Self


class Vector(tuple):  # type: ignore
    def __add__(self: Self, other: Self) -> "Vector":  # type: ignore
        return Vector(it.starmap(op.add, zip(self, other)))  # type: ignore


def V(*args: tuple[Any]):
    return Vector(args)


DIRS = N, S, W, E, NE, NW, SE, SW = (
    V(-1, 0),  # type: ignore
    V(1, 0),  # type: ignore
    V(0, -1),  # type: ignore
    V(0, 1),  # type: ignore
    V(-1, 1),  # type: ignore
    V(-1, -1),  # type: ignore
    V(1, 1),  # type: ignore
    V(1, -1),  # type: ignore
)
CHECK = deque([(0, 4, 5), (1, 6, 7), (2, 5, 7), (3, 4, 6)])


def parse_input(in_path: Path) -> set[Vector]:
    elves: set[Vector] = set()
    with in_path.open() as in_file:
        for y, line in enumerate(in_file):
            for x, tile in enumerate(line.strip()):
                if tile == "#":
                    elves.add(V(y, x))  # type: ignore

    return elves


def simulate(elves: set[Vector], checks: deque) -> bool:  # type: ignore
    moved = False
    proposals: dict[Vector, list[Vector]] = defaultdict(list)
    for elf in elves:
        free = [elf + delta not in elves for delta in DIRS]
        if all(free):
            continue

        for left, mid, right in checks:  # type: ignore
            if all((free[left], free[mid], free[right])):  # type: ignore
                proposal = elf + DIRS[left]  # type: ignore
                proposals[proposal].append(elf)  # type: ignore
                break

    for where, who in proposals.items():  # type: ignore
        if len(who) > 1:  # type: ignore
            continue
        moved = True
        elves.add(where)  # type: ignore
        elves.remove(who.pop())  # type: ignore

    return moved


def solve_p1(elves: set[Vector]) -> int:
    elves = elves.copy()
    checks = CHECK.copy()

    for _ in range(10):
        simulate(elves, checks)
        checks.rotate(-1)

    rows = [e[0] for e in elves]  # type: ignore
    cols = [e[1] for e in elves]  # type: ignore
    min_r, max_r = min(rows), max(rows) + 1  # type: ignore
    min_c, max_c = min(cols), max(cols) + 1  # type: ignore

    return (max_r - min_r) * (max_c - min_c) - len(elves)  # type: ignore


def solve_p2(elves: set[Vector]) -> int:  # type: ignore
    checks = CHECK.copy()
    for idx in it.count(1):
        if not simulate(elves, checks):
            return idx
        checks.rotate(-1)


if __name__ == "__main__":
    in_file = Path(__file__).parent.joinpath("input.txt")
    elves = parse_input(in_file)

    # Part 1
    print(f"Empty ground tiles: {solve_p1(elves)}")

    # Part 2
    print(f"First round with no movement: {solve_p2(elves)}")
