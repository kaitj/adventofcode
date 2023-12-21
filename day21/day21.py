#!/usr/bin/env python
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from aoc.utils import day_parser


@dataclass
class Position:
    y: int
    x: int

    def __hash__(self):
        return hash((self.y, self.x))

    def __add__(self, other: "Position") -> "Position":
        return Position(y=self.y + other.y, x=self.x + other.x)


class Direction(Enum):
    Up = Position(y=-1, x=0)
    Down = Position(y=1, x=0)
    Right = Position(y=0, x=1)
    Left = Position(y=0, x=-1)


class Day21:
    def __init__(self, input_path: str):
        self.map = self.load_map(input_path)

    def load_map(self, input_path: str) -> dict[Position, bool]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            map: dict[Position, bool] = {}

            for y, line in enumerate(in_file):
                if y == 0:
                    self.height = self.width = len(line.strip())
                for x, ch in enumerate(line.strip()):
                    map[Position(y, x)] = ch == "#"

                    if "S" in line:
                        self.start = Position(x=line.index("S"), y=y)
        return map

    def is_rock(self, position: Position) -> bool:
        small_position = Position(y=position.y % self.height, x=position.x % self.width)
        return self.map[small_position]

    def get_neighbours(self, pos: Position) -> list[Position]:
        return [pos + dir.value for dir in Direction._member_map_.values()]

    def get_garden_neighbours(self, pos: Position) -> list[Position]:
        garden_neighbours = [
            neighbour
            for neighbour in self.get_neighbours(pos)
            if neighbour in self.map.keys() and not self.map[neighbour]
        ]
        return garden_neighbours

    def get_reachable_positions(self, steps: int) -> set[Position]:
        reachable = {self.start}
        for _ in range(steps):
            new_reachable: set[Position] = set()
            for position in reachable:
                new_reachable.update(self.get_garden_neighbours(position))
                reachable = new_reachable
        return reachable

    def step(self, positions: set[Position]) -> set[Position]:
        new_positions: set[Position] = set()
        for position in positions:
            for neighbour in self.get_neighbours(position):
                if not self.is_rock(neighbour):
                    new_positions.add(neighbour)
        return new_positions

    def count_reachable_positions(self, steps: int) -> int:
        if steps % 2 == 0:
            starting_positions = {self.start}
        else:
            starting_positions = {
                neighbour
                for neighbour in self.get_neighbours(self.start)
                if not self.is_rock(neighbour)
            }

        prev_new_gardens: set[Position] = set()
        curr_new_gardens: set[Position] = starting_positions
        reached_count = len(starting_positions)

        for _ in range(steps // 2):
            one_step = self.step(positions=curr_new_gardens)
            two_step = self.step(positions=one_step)

            next_new_gardens = two_step - curr_new_gardens - prev_new_gardens

            reached_count += len(next_new_gardens)
            prev_new_gardens = curr_new_gardens
            curr_new_gardens = next_new_gardens

        return reached_count

    def process(self, steps: int) -> int:
        if steps < 2 * self.width:
            return self.count_reachable_positions(steps=steps)

        remainder = steps % self.width
        ys: list[int] = []
        xs: list[int] = []
        for run in range(3):
            n_steps = self.width * run + remainder
            reached_count = self.count_reachable_positions(n_steps)
            xs.append(n_steps)
            ys.append(reached_count)
            # breakpoint()

        a, b, c = self.fit(xs, ys)

        return round(a * steps**2 + b * steps + c)

    def fit(self, xs: list[int], ys: list[int]) -> tuple[float, float, float]:
        if xs[-1] - xs[-2] != xs[-2] - xs[-3]:
            raise NotImplementedError("xs should be equally spaced")

        a = (ys[-1] - 2 * ys[-2] + ys[-3]) / (
            xs[-1] ** 2 - 2 * xs[-2] ** 2 + xs[-3] ** 2
        )
        b = (ys[-1] - ys[-2] - a * xs[-1] ** 2 + a * xs[-2] ** 2) / (xs[-1] - xs[-2])
        c = ys[-1] - a * xs[-1] ** 2 - b * xs[-1]
        return a, b, c


class TestMain:
    def test_part1(self) -> None:
        test = Day21(f"{Path(__file__).parent}/test_input_part1.txt")
        assert len(test.get_reachable_positions(steps=6)) == 16

    def test_part2(self) -> None:
        test = Day21(f"{Path(__file__).parent}/input.txt")
        print(test.process(steps=26501365))


def main():
    args = day_parser().parse_args()

    solution = Day21(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(len(solution.get_reachable_positions(steps=64)))
    elif args.part == 2:
        print(solution.process(steps=26501365))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
