#!/usr/bin/env python
import operator as op
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import ClassVar, Self

from aoc.utils import day_parser


class Day02:
    OP: ClassVar[dict[int, Callable[[int, int], int] | bool]] = {
        1: op.add,
        2: op.mul,
        99: False,
    }

    def __init__(self: Self, input_path: str):
        self.program = self.parse_input(input_path)

    def parse_input(self: Self, input_path: str) -> list[int]:
        with Path(input_path).open() as in_file:
            return list(map(int, in_file.read().split(",")))

    def process_code(self: Self, code: list[int]) -> None:
        opcode, in_pos1, in_pos2, out_pos = code

        if opcode in [1, 2]:
            self.program[out_pos] = self.OP[opcode](  # type: ignore
                self.program[in_pos1], self.program[in_pos2]
            )
        else:
            raise ValueError("Invalid opcode")

    def process_program(self: Self, noun: int, verb: int, *, step: int = 4) -> None:
        self.program[1] = noun
        self.program[2] = verb
        for idx in range(0, len(self.program), step):
            if self.program[idx] == 99:
                break
            self.process_code(self.program[idx : idx + step])
        return None


class TestMain:
    def test_part1(self: Self) -> None:
        test = Day02(f"{Path(__file__).parent}/test_input_part1.txt")
        test.process_program(test.program[1], test.program[2])
        assert test.program[0] == 3500

    def test_part2(self: Self) -> None:
        ...
        # test = Day02(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day02(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        solution.process_program(12, 2)
        print(solution.program[0])
    elif args.part == 2:
        for noun in range(100):
            for verb in range(100):
                solution_copy = deepcopy(solution)
                solution_copy.process_program(noun, verb)
                if solution_copy.program[0] == 19690720:
                    print(100 * noun + verb)
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
