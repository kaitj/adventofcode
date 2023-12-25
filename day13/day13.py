#!/usr/bin/env python
from collections.abc import Sequence
from pathlib import Path

from aoc.utils import day_parser


class Day13:
    def __init__(self, input_path: str):
        self.valleys = self.load_valleys(input_path)

    def transpose(self, valley: Sequence[str]) -> list[str]:
        return ["".join(line) for line in zip(*valley)]

    def diff(self, line1: str, line2: str) -> int:
        return sum(1 for ch1, ch2 in zip(line1, line2) if ch1 != ch2)

    def load_valleys(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            contents = in_file.read().strip()
        valleys = contents.split("\n\n")
        valleys = [[*valley.split("\n")] for valley in valleys]

        return valleys

    def find_mirror(self, valley: list[str], no_smudges: int) -> int:
        length = len(valley[0])
        max_mirror_size = length // 2

        for midx in reversed(range(1, max_mirror_size + 1)):
            for shift in [0, length - 2 * midx]:
                smudges = no_smudges
                for row in valley:
                    smudges -= self.diff(
                        row[shift : shift + midx],
                        row[shift + midx : shift + 2 * midx][::-1],
                    )

                if smudges != 0:
                    continue

                return shift + midx

        return 0

    def summarize(self, no_smudges: int = 0) -> list[int]:
        # Find vertical
        vert = [self.find_mirror(valley, no_smudges) for valley in self.valleys]
        # Find horizontal
        horz = [
            100 * self.find_mirror(self.transpose(valley), no_smudges)
            for valley in self.valleys
        ]

        valleys_summary = [v_vert + v_horz for v_vert, v_horz in zip(vert, horz)]

        return valleys_summary


class TestMain:
    def test_part1(self) -> None:
        test = Day13(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.find_mirror(test.valleys[0], 0) == 5
        assert test.find_mirror(test.transpose(test.valleys[1]), 0) == 4
        assert sum(test.summarize()) == 405

    def test_part2(self) -> None:
        test = Day13(f"{Path(__file__).parent}/test_input_part1.txt")
        assert sum(test.summarize(no_smudges=1)) == 400


def main():
    args = day_parser().parse_args()

    solution = Day13(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(sum(solution.summarize()))
    elif args.part == 2:
        print(sum(solution.summarize(no_smudges=1)))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
