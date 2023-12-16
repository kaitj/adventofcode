#!/usr/bin/env python
from pathlib import Path

from aoc.utils import day_parser

DIRECTIONS: dict[str, tuple[int, int]] = {
    "r": (1, 0),
    "l": (-1, 0),
    "u": (0, -1),
    "d": (0, 1),
}


class Day16:
    def __init__(self, input_path: str):
        self.floor = self.load_floor(input_path)
        self.ROWS = len(self.floor)
        self.COLS = len(self.floor[0])

    def load_floor(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            return [[*line.strip()] for line in in_file]

    def _valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.COLS and 0 <= y < self.ROWS

    def _change_dir(self, direction: str, turn: str) -> str:
        turns = {
            "r": {"l": "u", "r": "d"},
            "l": {"l": "d", "r": "u"},
            "u": {"l": "r", "r": "l"},
            "d": {"l": "l", "r": "r"},
        }
        return turns[direction][turn]

    def find_direction(self, nx: int, ny: int, direction: str = "r") -> str:
        if (ch := self.floor[ny][nx]) == "/":
            return self._change_dir(direction, "l")
        elif ch == "\\":
            return self._change_dir(direction, "r")
        elif direction in "rl" and ch == "|":
            return "ud"
        elif direction in "ud" and ch == "-":
            return "rl"
        return direction

    def energize(self) -> set[tuple[int, int]]:
        visited: set[tuple[int, int, str]] = set()
        direction = self.find_direction(0, 0)
        q = [(0, 0, direction)]  # current location + current direction
        while q:
            cx, cy, direction = q.pop()
            visited.add((cx, cy, direction))
            dx, dy = DIRECTIONS[direction]  # pyright: ignore
            nx, ny = cx + dx, cy + dy

            if not self._valid_move(nx, ny):
                continue
            direction = self.find_direction(nx, ny, direction)
            if (nx, ny, direction) in visited:
                continue
            if len(direction) > 1:
                for next_dir in direction:
                    q.append((nx, ny, next_dir))
            else:
                q.append((nx, ny, direction))

        return {(nx, ny) for (nx, ny, _) in visited}


class TestMain:
    def test_part1(self) -> None:
        test = Day16(f"{Path(__file__).parent}/test_input_part1.txt")
        assert len(test.energize()) == 46

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day16(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day16(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(len(solution.energize()))
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
