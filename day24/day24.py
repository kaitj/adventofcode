#!/usr/bin/env python
import itertools as it
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

from aoc.utils import day_parser


@dataclass
class Vector:
    x: int | float
    y: int | float
    z: int | float


@dataclass
class Hailstone:
    position: Vector
    velocity: Vector

    def __repr__(self):
        return f"Position: {self.position} @ Velocity: {self.velocity}"

    def is_parallel(self, other: "Hailstone") -> bool:
        return self.velocity.y * other.velocity.x == self.velocity.x * other.velocity.y

    def find_intersect(self, other: "Hailstone", *, amin: int, amax: int) -> int:
        if self.is_parallel(other):
            return 0

        t1 = (
            other.velocity.y * (self.position.x - other.position.x)
            - other.velocity.x * (self.position.y - other.position.y)
        ) / (self.velocity.y * other.velocity.x - self.velocity.x * other.velocity.y)
        t2 = (
            self.velocity.y * (other.position.x - self.position.x)
            - self.velocity.x * (other.position.y - self.position.y)
        ) / (other.velocity.y * self.velocity.x - other.velocity.x * self.velocity.y)

        # If cross in the past
        if t1 < 0 or t2 < 0:
            return 0

        x = self.position.x + self.velocity.x * t1
        y = self.position.y + self.velocity.y * t1

        if amin <= x <= amax and amin <= y <= amax:
            return 1

        # Crossed outside
        return 0


class Day24:
    def __init__(self, input_path: str):
        self.hailstones = self.load_hailstones(input_path)

    def load_hailstones(self, input_path: str) -> list[Hailstone]:
        hailstones: list[Hailstone] = []
        with Path(input_path).open(encoding="utf-8") as in_file:
            for line in in_file:
                positions, velocities = line.strip().split(" @ ")
                hailstones.append(
                    Hailstone(
                        position=Vector(*map(int, positions.split(","))),
                        velocity=Vector(*map(int, velocities.split(","))),
                    )
                )

        return hailstones

    def find_intersections(self, *, amin: int, amax: int) -> int:
        return sum(
            [
                hailstone1.find_intersect(hailstone2, amin=amin, amax=amax)
                for hailstone1, hailstone2 in it.combinations(self.hailstones, 2)
            ]
        )

    def find_position(self, /, h1: Hailstone, h2: Hailstone, h3: Hailstone) -> int:
        x, y, z, vx, vy, vz = (sp.Symbol(ch) for ch in "x,y,z,vx,vy,xz".split(","))
        pos = [x, y, z]
        vel = [vx, vy, vz]
        vars = [*pos, *vel]
        eqns = []

        for idx, hs in enumerate([h1, h2, h3]):
            hs_pos = [hs.position.x, hs.position.y, hs.position.z]
            hs_vel = [hs.velocity.x, hs.velocity.y, hs.velocity.z]
            t = sp.Symbol(f"t_{idx}")

            for jidx in range(3):
                eqns.append(  # type: ignore
                    pos[jidx]
                    + vel[jidx] * t  # type: ignore
                    - (hs_pos[jidx] + hs_vel[jidx] * t)  # type: ignore
                )
            vars.append(t)  # type: ignore

        return int(sum(sp.solve_poly_system(eqns, vars)[0][:3]))  # type: ignore


class TestMain:
    def test_part1(self) -> None:
        test = Day24(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.find_intersections(amin=7, amax=27) == 2

    def test_part2(self) -> None:
        test = Day24(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.find_position(*test.hailstones[:3]) == 47


def main():
    args = day_parser().parse_args()

    solution = Day24(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(solution.find_intersections(amin=200000000000000, amax=400000000000000))
    elif args.part == 2:
        print(solution.find_position(*solution.hailstones[:3]))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
