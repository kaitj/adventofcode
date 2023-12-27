from pathlib import Path


def parse_input(in_fpath: Path) -> list[list[int]]:
    with in_fpath.open() as in_file:
        cave = [list(map(int, line.strip())) for line in in_file]

    return cave


def repeat(cave: list[list[int]], x: int, y: int, width: int, height: int) -> int:
    r = int(cave[y % height][x % width])
    b = int(x / width) + int(y / height)

    return int((r + b) / 10) + (r + b) % 10


def get_neighbours(x: int, y: int, width: int, height: int, r: int = 1):
    if x > 0:
        yield (x - 1, y)
    if x < r * width - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < r * height - 1:
        yield (x, y + 1)


def est_len(x: int, y: int, sofar: int, r: int = 1) -> int:
    return sofar + r * width - 1 - x + r * height - 1 - y


def get_path_length(cave: list[list[int]], r: int, width: int, height: int) -> int:
    q = {(0, 0): (0, est_len(0, 0, 0))}
    seen: dict[tuple[int, int], tuple[int, int]] = {}

    while (width * r - 1, height * r - 1) not in seen:
        x, y = min(q, key=lambda a: q[a][1])  # type: ignore
        d, e = q[x, y]  # type: ignore
        seen[x, y] = d, e  # type: ignore
        del q[x, y]

        for v, w in get_neighbours(x, y, r, width, height):
            if (v, w) not in seen:
                d00 = min(
                    q.get((v, w), (999999999999, 0))[0],  # type: ignore
                    d + repeat(cave, v, w, width, height),
                )
                q[v, w] = d00, est_len(v, w, d00, r)  # type:ignore

    return seen[width * r - 1, height * r - 1][0]  # type: ignore


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    cave = parse_input(in_fpath)
    width = len(cave[0])
    height = len(cave)

    # Puzzle 1
    print(f"Answer: {get_path_length(cave, 1, width, height)}")

    # Puzzle 2
    print(f"Answer: {get_path_length(cave, 5, width, height)}")
