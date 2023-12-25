#!/usr/bin/env python
from collections import namedtuple
import itertools as it
from operator import lshift, rshift
from pathlib import Path
from typing import Any, Self


class Rock:
    __slots__ = ["ints", "len", "i", "pos"]

    def __init__(self: Self, ints: list[int], i: int, pos: int = 0b0010000):
        self.ints = ints
        self.len = len(self.ints)
        self.i = i
        self.pos = pos

    def shift(self: Self, jet: str) -> "Rock":
        op = {">": rshift, "<": lshift}[jet]
        return Rock([op(i, 1) for i in self.ints], self.i, op(self.pos, 1))

    def overlaps(self: Self, pile: int) -> bool:
        for i, layer in zip(self.ints, pile):  # type: ignore
            if i & layer:
                return True

        return False

    def shiftable(self, jet: str) -> bool:
        edge = {">": 0b0000001, "<": 0b1000000}[jet]
        for i in self.ints:
            if i & edge:
                return False
        return True


ROCKS = (
    Rock((0b0011110,), 0),  # type: ignore
    Rock((0b0001000, 0b0011100, 0b0001000), 1),  # type: ignore
    Rock((0b0000100, 0b0000100, 0b0011100), 2),  # type: ignore
    Rock((0b0010000, 0b0010000, 0b0010000, 0b0010000), 3),  # type: ignore
    Rock((0b0011000, 0b0011000), 4),  # type: ignore
)


def read_input(in_file: str) -> list[Any]:
    Jet = namedtuple("Jet", ["i", "dir"])  # type: ignore

    with Path(in_file).open(encoding="utf-8") as in_path:
        in_str = in_path.read().strip()
    return list(it.starmap(Jet, enumerate(in_str)))


def solve(jets: list[Any], total: int = 2022, part2: bool = False):  # type: ignore
    Previous = namedtuple("Previous", ["rock", "height"])  # type: ignore
    rocks, jets = it.cycle(ROCKS), it.cycle(jets)  # type: ignore
    pile = [0] * 10000
    top = len(pile)
    states = {}

    for n_rock in it.count():
        rock = next(rocks)
        for y in it.count(top - rock.len - 3):
            jet = next(jets)  # type: ignore
            if rock.shiftable(jet.dir):  # type: ignore
                shifted = rock.shift(jet.dir)  # type: ignore
                if not shifted.overlaps(pile[y:]):  # type: ignore
                    rock = shifted
            if rock.overlaps(pile[y + 1 :]) or rock.len + y >= len(pile):  # type: ignore
                for i in range(rock.len):
                    pile[y + i] |= rock.ints[i]
                break
        top = min(top, y)  # type: ignore
        height = len(pile) - top

        state = (jet.i, rock.i, rock.pos)  # type: ignore
        if prev := states.get(state):  # type: ignore
            rcycle = n_rock - prev.rock  # type: ignore
            hcycle = height - prev.height  # type: ignore
            diff = total - n_rock - 1
            more, remain = divmod(diff, rcycle)  # type: ignore
            if remain == 0:
                return hcycle * more + height  # type: ignore
        else:
            states[state] = Previous(n_rock, height)


if __name__ == "__main__":
    in_file = str(Path(__file__).parent.joinpath("input.txt"))
    jets = read_input(in_file)

    # Part 1
    print(f"Height of tower of rocks: {solve(jets=jets)}")

    # Part 2
    print(
        f"Height of tower of rocks: "
        f"{solve(jets=jets, total=1_000_000_000_000, part2=True)}"
    )
