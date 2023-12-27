import re
from pathlib import Path


def parse_input(in_fpath: Path) -> tuple[int, ...]:
    with in_fpath.open() as in_file:
        xmin, xmax, ymin, ymax = map(int, re.findall(r"-?\d+", in_file.read().strip()))

    return xmin, xmax, ymin, ymax


def solve_p1(ymin: int) -> int:
    return (ymin + 1) * ymin // 2


def solve_p2(xmin: int, xmax: int, ymin: int, ymax: int) -> int:
    v, n = 0, int((xmin * 2) ** 0.5 - 1)  # n-th member of arithmetic progression

    for dy_init in range(ymin, -ymin):
        for dx_init in range(n, xmax + 1):
            x, y, dx, dy = 0, 0, dx_init, dy_init
            while x <= xmax and y >= ymin and (dx == 0 and xmin <= x or dx != 0):
                x += dx
                y += dy
                if dx > 0:
                    dx -= 1
                dy -= 1
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    v += 1
                    break

    return v


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    xmin, xmax, ymin, ymax = parse_input(in_fpath)

    print(f"Answer: {solve_p1(ymin)}")
    print(f"Answer: {solve_p2(xmin, xmax, ymin, ymax)}")
