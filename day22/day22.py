#!/usr/bin/env python
from dataclasses import dataclass
from pathlib import Path

from aoc.utils import day_parser


@dataclass
class Position:
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash((self.x, self.y, self.z))


@dataclass
class Brick:
    start: Position
    end: Position

    def __hash__(self):
        return hash((self.start, self.end))


class Day22:
    def __init__(self, input_path: str):
        self.bricks = self.load_bricks(input_path)

    def load_bricks(self, input_path: str) -> list[Brick]:
        bricks: list[Brick] = []
        with Path(input_path).open(encoding="utf-8") as in_file:
            for line in in_file:
                start, end = line.strip().split("~")
                bricks.append(
                    Brick(
                        start=Position(*map(int, start.split(","))),
                        end=Position(*map(int, end.split(","))),
                    )
                )

        # Return order in "ascending" order
        return sorted(bricks, key=lambda brick: brick.start.z)  # type: ignore

    def update_position(self, brick: Brick, distance: int) -> Brick:
        return Brick(
            start=Position(
                x=brick.start.x, y=brick.start.y, z=brick.start.z - distance
            ),
            end=Position(x=brick.end.x, y=brick.end.y, z=brick.end.z - distance),
        )

    def simulate(self, update: bool = False, without: Brick | None = None):
        n_fell = 0
        heights: dict[tuple[int, int], int] = {}

        for bidx, brick in enumerate(self.bricks):
            new_height = None
            if brick != without:
                xys = [
                    (x, y)
                    for x in range(brick.start.x, brick.end.x + 1)
                    for y in range(brick.start.y, brick.end.y + 1)
                ]
                height = max(heights.get(xy, 0) for xy in xys)
                dist = brick.start.z - height - 1

                if dist:
                    n_fell += 1
                    new_height = brick.end.z - dist
                    if update:
                        self.bricks[bidx].start.z -= dist
                        self.bricks[bidx].end.z -= dist

                for xy in xys:
                    heights[xy] = new_height if new_height else brick.end.z

        return n_fell


class TestMain:
    def test_part1(self) -> None:
        test = Day22(f"{Path(__file__).parent}/test_input_part1.txt")
        test.simulate(update=True)
        test_drop_counts = [test.simulate(without=brick) for brick in test.bricks]
        assert test_drop_counts.count(0) == 5

    def test_part2(self) -> None:
        test = Day22(f"{Path(__file__).parent}/test_input_part1.txt")
        test.simulate(update=True)
        test_drop_counts = [test.simulate(without=brick) for brick in test.bricks]
        assert sum(test_drop_counts) == 7


def main():
    args = day_parser().parse_args()

    solution = Day22(f"{Path(__file__).parent}/input.txt")
    solution.simulate(update=True)
    brick_drop_counts = [solution.simulate(without=brick) for brick in solution.bricks]
    if args.part == 1:
        print(brick_drop_counts.count(0))
    elif args.part == 2:
        print(sum(brick_drop_counts))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
