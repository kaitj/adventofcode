import re
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, Self


@dataclass
class Point:
    x: int
    y: int
    z: int


class Instruction(NamedTuple):
    value: bool
    cuboid: "Cuboid"


class Cuboid:
    def __init__(self: Self, corner1: Point, corner2: Point):
        self.c1 = corner1
        self.c2 = corner2

    def is_valid(self) -> bool:
        return (
            (self.c1.x < self.c2.x)
            and (self.c1.y < self.c2.y)
            and (self.c1.z < self.c2.z)
        )

    @property
    def volume(self) -> int:
        return (
            (self.c2.x - self.c1.x) * (self.c2.y - self.c1.y) * (self.c2.z - self.c1.z)
        )


def get_overlap(a: Cuboid, b: Cuboid) -> Cuboid | None:
    overlap = Cuboid(
        Point(max(a.c1.x, b.c1.x), max(a.c1.y, b.c1.y), max(a.c1.z, b.c1.z)),
        Point(min(a.c2.x, b.c2.x), min(a.c2.y, b.c2.y), min(a.c2.z, b.c2.z)),
    )

    return overlap if overlap.is_valid() else None


def parse_input(in_fpath: Path) -> list[Instruction]:
    regex = re.compile(
        r"(on|off) x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+)"
    )
    instructions: list[Instruction] = []
    with in_fpath.open() as in_file:
        for line in in_file:
            if match := regex.search(line):
                value = match[1] == "on"
                pt1 = Point(int(match[2]), int(match[4]), int(match[6]))
                pt2 = Point(int(match[3]), int(match[5]), int(match[7]))
                pt2 = Point(pt2.x + 1, pt2.y + 1, pt2.z + 1)
                cuboid = Cuboid(pt1, pt2)
                instructions.append(Instruction(value, cuboid))
    return instructions


def run_p1(instructions: list[Instruction]) -> int:
    p1_instructions: list[Instruction] = []
    region = Cuboid(Point(-50, -50, -50), Point(51, 51, 51))

    for instruction in instructions:
        if overlapping := get_overlap(region, instruction.cuboid):
            p1_instructions.append(Instruction(instruction.value, overlapping))

    return run_instructions(p1_instructions)


def run_instructions(instructions: list[Instruction]) -> int:
    placed: list[Cuboid] = []
    volume = 0

    for instruction in reversed(instructions):
        if instruction.value:
            overlaps: list[Instruction] = []
            for cuboid in placed:  # type: ignore
                if (
                    overlapping := get_overlap(cuboid, instruction.cuboid)  # type: ignore
                ) is not None:
                    overlaps.append(Instruction(True, overlapping))
            volume += instruction.cuboid.volume - run_instructions(overlaps)  # type: ignore

        placed.append(instruction.cuboid)

    return volume


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    instructions = parse_input(in_fpath)

    print(f"Answer: {run_p1(instructions)}")
    print(f"Answer: {run_instructions(instructions)}")
