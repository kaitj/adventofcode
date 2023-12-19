#!/usr/bin/env python
import re
from pathlib import Path

from aoc.utils import day_parser


class Day19:
    def __init__(self, input_path: str):
        self.workflows, self.ratings = self.load_workflows(input_path)

    def load_workflows(
        self, input_path: str
    ) -> tuple[dict[str, dict[str, list[list[str]]]], dict[int, dict[str, int]]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            workflows, ratings = in_file.read().split("\n\n")

        workflows = {
            key: conditions
            for workflow in workflows.strip().split("\n")
            for key, conditions in re.findall(r"([a-z]+){(\S+)}", workflow)
        }

        ratings = {
            idx: {key: int(val) for key, val in re.findall(r"([a-z])=(\d+)", rating)}
            for idx, rating in enumerate(ratings.strip().split("\n"))
        }

        return workflows, ratings

    def run_workflow(self, ratings: dict[str, int], step: str = "in") -> int:
        # Assign rating to string variable key
        for key, rating in ratings.items():
            vars()[key] = rating
        while step not in "AR":
            condition, result = self.workflows[step].split(":", 1)  # pyright: ignore
            accept, reject = result.split(",", 1)  # pyright: ignore
            if eval(condition):  # pyright: ignore
                step = accept  # pyright: ignore
            else:
                step = reject  # pyright: ignore
                while ":" in step:
                    condition, result = step.split(":", 1)  # pyright: ignore
                    accept, reject = result.split(",", 1)  # pyright: ignore
                    step = accept if eval(condition) else reject  # pyright: ignore

        return sum(ratings.values()) if step == "A" else 0

    def run_workflows(self) -> list[int]:
        return [self.run_workflow(ratings=rating) for rating in self.ratings.values()]


class TestMain:
    def test_part1(self) -> None:
        test = Day19(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.run_workflow(test.ratings[0]) == 7540
        assert test.run_workflow(test.ratings[2]) == 4623
        assert test.run_workflow(test.ratings[4]) == 6951
        assert sum(test.run_workflows()) == 19114

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day19(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day19(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(sum(solution.run_workflows()))
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
