#!/usr/bin/env python
from pathlib import Path

# Map describing how pipes can be connected with next position
VALID_MOVES = {
    "-": [(0, 1), (0, -1)],
    "|": [(1, 0), (-1, 0)],
    "L": [(0, 1), (-1, 0)],
    "F": [(0, 1), (1, 0)],
    "7": [(0, -1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
}
PIPE_MAP = {
    (1, 0): "|LJ",
    (-1, 0): "|7F",
    (0, -1): "-LF",
    (0, 1): "-7J",
}
SKIP_MAP = {
    "F": "7",
    "L": "J",
}


class Day10:
    def __init__(self, input_path: str):
        self.maze = self.load_maze(input_path)
        self.visited: set[tuple[int, int]] = set()
        self.ROWS = len(self.maze)
        self.COLS = len(self.maze[0])

    def load_maze(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            maze = [[*line.strip()] for line in in_file]

        return maze

    def find_start_pos(self) -> tuple[int, int]:
        for y, line in enumerate(self.maze):
            if "S" in line:
                x = "".join(line).index("S")
                return (y, x)

        raise LookupError("No starting position found")

    def find_max_distance(self) -> int:
        y, x = self.find_start_pos()

        self.visited.add(start := (y, x))
        for dy, dx in PIPE_MAP:
            if self.maze[y + dy][x + dx] in PIPE_MAP[(dy, dx)]:  # pyright: ignore
                cur = (y + dy, x + dx)
        prev = start
        while cur != start:  # pyright: ignore
            self.visited.add(cur)  # pyright: ignore
            (y, x) = cur  # pyright: ignore
            for dy, dx in VALID_MOVES[self.maze[y][x]]:  # pyright: ignore
                nxt = (y + dy, x + dx)  # pyright: ignore
                if nxt != prev:
                    prev = cur  # pyright: ignore
                    cur = nxt  # pyright: ignore
                    break

        return len(self.visited) // 2

    def find_enclosed_area(self) -> int:
        area = 0
        for y in range(self.ROWS):
            parity = 0
            for x in range(self.COLS):
                # If ground or junk pipe
                if (y, x) not in (self.visited):
                    if parity % 2 == 1:
                        area += 1
                    continue

                if self.maze[y][x] in "|LJ":
                    parity += 1

        return area


class TestMain:
    def test_part1(self):
        test = Day10(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.find_max_distance() == 8

    def test_part2(self):
        test = Day10(f"{Path(__file__).parent}/test_input_part2.txt")
        test.find_max_distance()
        assert test.find_enclosed_area() == 10


if __name__ == "__main__":
    solution = Day10(f"{Path(__file__).parent}/input.txt")
    print(solution.find_max_distance())
    print(solution.find_enclosed_area())
