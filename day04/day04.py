from dataclasses import dataclass
from typing import NamedTuple

import utils


class Coord(NamedTuple):
    """New type storing location on bingo board"""

    x: int
    y: int


@dataclass
class Square:
    """Data type storing information about element on bingo board"""

    num: int
    coord: Coord
    drawn: bool


def get_draw(list_nums: list[str]) -> list[int]:
    """Get bingo draw numbers"""
    return [int(val) for val in list_nums.split(",")]


def gen_boards(in_boards: list[str]) -> list[dict[int, int, bool]]:
    """Generate all boards with ability to track if they have been drawn"""
    boards = [
        {
            Coord(x, y): Square(int(val), Coord(x, y), False)
            for y, line in enumerate(board.split("\n"))
            for x, val in enumerate(line.split())
        }
        for board in in_boards
    ]

    return boards


BINGO = [
    *({Coord(x, y) for y in range(5)} for x in range(5)),
    *({Coord(x, y) for x in range(5)} for y in range(5)),
]


def check_bingo(board: dict[int, int, bool]) -> bool:
    """Check if all elements in rows or columns match drawn 
    numbers in any of the bingo boards"""
    return any(all(board[coord].drawn for coord in combo) for combo in BINGO)


def play_bingo(
    draw_nums: list[int], boards: list[dict[int, int, bool]], last: bool = False
):
    fin_board = set()
    for draw in draw_nums:
        for board in boards:
            # If uniq card done, move on
            if id(board) in fin_board:
                continue

            square = [val for val in board.values() if val.num == draw]
            # If num not found on board, move on, otherwise mark as drawn
            if not square:
                continue
            square[0].drawn = True

            if check_bingo(board):
                # If looking for first winning board
                if not last:
                    return board, draw

                # Find last winning board
                fin_board.add(id(board))
                if len(fin_board) == len(boards):
                    return board, draw


def solve(in_data: str, last: bool = False):
    draw_nums = get_draw(in_data[0])
    boards = gen_boards(in_data[1:])
    winning_board, draw = play_bingo(draw_nums, boards, last)

    return draw * sum(ele.num for ele in winning_board.values() if not ele.drawn)


if __name__ == "__main__":
    in_fpath = input("Enter path containing bingo: ")
    in_data = utils.parse_group(in_fpath)

    print(f"1. Final score: {solve(in_data)}")
    print(f"2. Final score: {solve(in_data, True)}")
