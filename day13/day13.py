#!/usr/bin/env python
from pathlib import Path

from aoc.utils import day_parser


class Day13:
    def __init__(self, input_path: str):
        self.valleys = self.load_valleys(input_path)

    def load_valleys(self, input_path: str) -> list[list[str]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            contents = in_file.read()
        valleys = contents.split("\n\n")
        valleys = [[*valley.split("\n")] for valley in valleys]

        return valleys

    def find_mirror(self, valley: list[str]) -> int:
        """
        valley[idx] - right reflection
        line (or idx - 1) = left reflection
        """
        mirror = False
        for idx, line in enumerate(valley[:-1], start=1):
            # Found a possible reflection
            if valley[idx] == line:
                # Check left half == right half
                mirror = all(
                    left == right
                    for left, right in zip(valley[idx - 1 :: -1], valley[idx:])
                )

            if mirror:
                return idx

        return 0  # pyright: ignore

    def summarize(self) -> list[int]:
        # Find vertical
        vert = [self.find_mirror(list(zip(*valley))) for valley in self.valleys]
        # Find horizontal
        horz = [self.find_mirror(valley) for valley in self.valleys]

        valleys_summary = [v_vert + 100 * v_horz for v_vert, v_horz in zip(vert, horz)]

        return valleys_summary


class TestMain:
    def test_part1(self) -> None:
        test = Day13(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.find_mirror(list(zip(*test.valleys[0]))) == 5  # pyright: ignore
        assert test.find_mirror(test.valleys[1]) == 4  # pyright: ignore
        assert sum(test.summarize()) == 405

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day13(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day13(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(sum(solution.summarize()))
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
