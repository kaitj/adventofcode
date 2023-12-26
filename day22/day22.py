#!/usr/bin/env python
import re
import itertools as it
import operator as op
from pathlib import Path
from typing import Any, Callable, Self


def process_board(board_str: list[str]) -> dict[tuple[int, int], str]:
    board: dict[tuple[int, int], str] = {}
    for i, s in enumerate(board_str):
        for j, c in enumerate(s):
            if c != " ":
                board[(i + 1, j + 1)] = c
    return board


def process_path(path_str: str) -> list:
    idx = [0] + [i for i, c in enumerate(path_str) if c in ["L", "R"]] + [len(path_str)]
    slices = [path_str[s:e] for s, e in list(zip(idx[:-1], idx[1:]))]
    path = []
    for i, s in enumerate(slices):
        if i == 0:
            dir = None
            n = int(s)
        else:
            dir = s[0]
            n = int(s[1:])
        path.append((dir, n))
    return path


def define_start(board: dict[tuple[int, int], str]) -> tuple[int, int]:
    top_cols = [j for i, j in board.keys() if i == 1]
    return (1, min(top_cols))


def _get_limit_positions(zones: dict, zone: int, facing: str, face_length: int) -> list:
    i, j = zones[zone]
    if facing == ">":
        return [
            (x + 1, (j + 1) * face_length)
            for x in range(i * face_length, (i + 1) * face_length)
        ]
    if facing == "v":
        return [
            ((i + 1) * face_length, y + 1)
            for y in range(j * face_length, (j + 1) * face_length)
        ]
    if facing == "<":
        return [
            (x + 1, j * face_length + 1)
            for x in range(i * face_length, (i + 1) * face_length)
        ]
    if facing == "^":
        return [
            (i * face_length + 1, y + 1)
            for y in range(j * face_length, (j + 1) * face_length)
        ]


def build_wrapping_cube(zones: dict, zone_mapping: dict, face_length: int) -> dict:
    mapping = {}
    for start, end in zone_mapping.items():
        start_zone, start_dir = start
        end_zone, end_dir, reverse = end
        start_ps = _get_limit_positions(
            zones=zones, zone=start_zone, facing=start_dir, face_length=face_length
        )
        rev_end_dir = (
            "v"
            if end_dir == "^"
            else ("^" if end_dir == "v" else (">" if end_dir == "<" else "<"))
        )
        end_ps = _get_limit_positions(
            zones=zones, zone=end_zone, facing=rev_end_dir, face_length=face_length
        )
        end_ps = end_ps if reverse != -1 else reversed(end_ps)
        for s, e in zip(start_ps, end_ps):
            mapping[(s, start_dir)] = (e, end_dir)
    return mapping


def wrap_board(board: dict, position: tuple, direction: str) -> tuple:
    i, j = position
    if direction in ["^", "v"]:
        rows = [x for x, y in board.keys() if y == j]
        return (min(rows) if direction == "v" else max(rows), j)
    if direction in [">", "<"]:
        cols = [y for x, y in board.keys() if x == i]
        return (i, min(cols) if direction == ">" else max(cols))


def follow_path(
    board: dict,
    path: list,
    directions: list = [">", "v", "<", "^"],
    start_dir_idx: int = 0,
    start: tuple = None,
    rock_symbol: str = "#",
    wrap_mapping: dict = None,
) -> tuple:
    i, j = start if start is not None else define_start(board)
    for turn, n in path:
        if turn is None:
            dir_idx = start_dir_idx
        else:
            dir_idx = (
                (dir_idx + 1) % len(directions)
                if turn == "R"
                else (dir_idx - 1) % len(directions)
            )
        d = directions[dir_idx]
        for _ in range(n):
            ni, nj = process_direction((i, j), d)
            nd, n_dir_idx = d, dir_idx
            if (ni, nj) not in board:
                if wrap_mapping is not None:
                    (ni, nj), nd = wrap_mapping[((i, j), d)]
                    n_dir_idx = directions.index(nd)
                else:
                    ni, nj = wrap_board(board, (ni, nj), d)
            if board[(ni, nj)] != rock_symbol:
                i, j, d, dir_idx = ni, nj, nd, n_dir_idx
            else:
                break
    return (i, j), d


def compute_password(
    board: dict,
    path: list,
    row_score: int = 1000,
    col_score: int = 4,
    dir_scores: dict = {">": 0, "v": 1, "<": 2, "^": 3},
    wrap_mapping: dict = None,
) -> int:
    (row, col), dir = follow_path(board, path, wrap_mapping=wrap_mapping)
    return row_score * row + col_score * col + dir_scores[dir]


def clean_string_list(l: str, drop_spaces: bool = True) -> list:
    def _clean_string(s: str) -> str:
        s = s.strip() if drop_spaces else s.replace("\n", "")
        return s if len(s) > 0 else None

    l = [
        (
            _clean_string(s)
            if not isinstance(s, list)
            else clean_string_list(s, drop_spaces=drop_spaces)
        )
        for s in l
    ]
    l = [s for s in l if s is not None]
    return l if len(l) > 0 else None


def read_file_into_list(
    path: str, split_list_char: str = None, drop_spaces: bool = True
) -> list:
    with open(path) as f:
        lines = f.readlines()
    if split_list_char is not None:
        cuts = [i for i, x in enumerate(lines) if x == split_list_char]
        cuts = [0] + cuts + [len(lines)]
        lines = [
            [s for s in lines[i:j]]
            for i, j in zip(cuts[: (len(cuts) - 1)], cuts[1 : len(cuts)])
        ]
    return clean_string_list(lines, drop_spaces=drop_spaces)


def process_direction(position: tuple, direction: str) -> tuple:
    i, j = position
    if direction == "^":
        return (i - 1, j)
    if direction == ">":
        return (i, j + 1)
    if direction == "v":
        return (i + 1, j)
    if direction == "<":
        return (i, j - 1)


if __name__ == "__main__":
    in_file = str(Path(__file__).parent.joinpath("input.txt"))
    in_board, in_path = read_file_into_list(
        path=in_file,
        drop_spaces=False,
        split_list_char="\n",
    )
    board = process_board(in_board)
    path = process_path(in_path[0])

    # Part 1
    print(f"Final password: {compute_password(board, path)}")

    # Part 2
    input_cube = {1: (0, 1), 2: (0, 2), 3: (1, 1), 4: (2, 0), 5: (2, 1), 6: (3, 0)}
    input_cube_mapping = {
        (1, "<"): (4, ">", -1),
        (1, "^"): (6, ">", 1),
        (2, "^"): (6, "^", 1),  ## !!!
        (2, ">"): (5, "<", -1),
        (2, "v"): (3, "<", 1),
        (3, "<"): (4, "v", 1),
        (3, ">"): (2, "^", 1),
        (4, "^"): (3, ">", 1),
        (4, "<"): (1, ">", -1),
        (5, ">"): (2, "<", -1),
        (5, "v"): (6, "<", 1),
        (6, "<"): (1, "v", 1),
        (6, "v"): (2, "v", 1),
        (6, ">"): (5, "^", 1),
    }
    cube_wrap = build_wrapping_cube(
        zones=input_cube, zone_mapping=input_cube_mapping, face_length=50
    )
    print(f"Final password: {compute_password(board, path, wrap_mapping=cube_wrap)}")
