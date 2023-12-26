#!/usr/bin/env python
from pathlib import Path


CHARMAP = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}


def parse_input(
    in_path: Path,
) -> tuple[list[str], ...]:
    with in_path.open() as in_file:
        content = in_file.read()

    return tuple(map(list, content.splitlines()))


def decimal(snafu: list[str]) -> int:
    if not snafu:
        return 0
    last = snafu.pop()
    return 5 * decimal(snafu) + CHARMAP[last]


def snafu(dec: int) -> str:
    if not dec:
        return ""
    q, r = divmod(dec + 2, 5)
    return snafu(q) + "=-012"[r]


if __name__ == "__main__":
    in_file = Path(__file__).parent.joinpath("input.txt")
    snafus = parse_input(in_file)

    num = snafu(sum(map(decimal, snafus)))

    # Part 1
    print(f"Answer: {num}")
