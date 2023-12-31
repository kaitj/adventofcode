import itertools as it
import re
from collections import Counter, defaultdict
from pathlib import Path


def parse_input(in_fpath: Path) -> list[int]:
    with in_fpath.open() as in_file:
        pos = [int(re.search(r"\d+$", line).group(0)) for line in in_file]  # type: ignore

    return pos


def wrap10(n: int) -> int:
    return n % 10 or 10


def practice(p1: int, p2: int, goal: int = 1000, rolls: int = 3) -> int:
    s1 = s2 = 0
    roll_count = 0
    dd = it.cycle(range(1, 101))

    while True:
        p1 = wrap10(p1 + sum(next(dd) for _ in range(rolls)))
        s1 += p1
        roll_count += rolls
        if s1 >= goal:
            break

        p2 = wrap10(p2 + sum(next(dd) for _ in range(rolls)))
        s2 += p2
        roll_count += rolls
        if s2 >= goal:
            break

    return min(s1, s2) * roll_count


def move_p1(
    verse: dict[tuple[int, ...], int], move_counts: list[tuple[int, int]]
) -> dict[tuple[int, ...], int]:
    next_verse: dict[tuple[int, ...], int] = defaultdict(int)
    for ((p1_score, p1_pos, p2_score, p2_pos), verse_count), (
        move,
        move_count,
    ) in it.product(verse.items(), move_counts):
        p1_pos = wrap10(p1_pos + move)
        p1_score += p1_pos
        next_verse[(p1_score, p1_pos, p2_score, p2_pos)] += verse_count * move_count

    return next_verse


def move_p2(
    verse: dict[tuple[int, ...], int], move_counts: list[tuple[int, int]]
) -> dict[tuple[int, ...], int]:
    next_verse: dict[tuple[int, ...], int] = defaultdict(int)
    for ((p1_score, p1_pos, p2_score, p2_pos), verse_count), (
        move,
        move_count,
    ) in it.product(verse.items(), move_counts):
        p2_pos = wrap10(p2_pos + move)
        p2_score += p2_pos
        next_verse[(p1_score, p1_pos, p2_score, p2_pos)] += verse_count * move_count

    return next_verse


def cull_wins(verse: dict[tuple[int, ...], int], completed: list[tuple[int, ...]]):
    for k in list(verse):
        (p1_score, _, p2_score, _) = k
        if p1_score >= 21 or p2_score >= 21:
            completed.append((p1_score, p2_score, verse[k]))
            del verse[k]


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    p1, p2 = parse_input(in_fpath)

    print(f"Answer: {practice(p1, p2)}")

    possible_moves = [sum(x) for x in it.product((1, 2, 3), repeat=3)]
    move_counts = sorted(Counter(possible_moves).items())
    verse = {(0, p1, 0, p2): 1}
    completed = []

    while verse:
        verse = move_p1(verse, move_counts)
        cull_wins(verse, completed)
        verse = move_p2(verse, move_counts)
        cull_wins(verse, completed)

    sol_2 = max(
        sum(c for (a, _, c) in completed if a >= 21),  # type: ignore
        sum(c for (_, b, c) in completed if b >= 21),  # type: ignore
    )

    print(f"Answer {sol_2}")
