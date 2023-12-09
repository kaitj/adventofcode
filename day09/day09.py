#!/usr/bin/env python
from pathlib import Path
from unittest import TestCase


class Day09:
    def __init__(self, input_path: str):
        self.histories = self.load_histories(input_path)

    def load_histories(self, input_path: str) -> list[list[int]]:
        with Path(input_path).open(encoding="utf-8") as in_file:
            histories = [
                list(map(int, line.strip().split()))  # pyright: ignore
                for line in in_file
            ]

        return histories

    def complete_history_sequence(self, history: list[int]) -> list[list[int]]:
        history_sequence = [history.copy()]

        # Complete sequence
        while any(
            diff := [
                b - a
                for a, b in zip(history_sequence[-1][:-1], history_sequence[-1][1:])
            ]
        ):
            history_sequence.append(diff)
        history_sequence.append(diff)

        no_seqs = len(history_sequence)
        # Fill in placeholders
        for idx in range(no_seqs - 1, -1, -1):
            if idx == no_seqs - 1:
                history_sequence[idx] = [0] + -1 * history_sequence[idx]
                history_sequence[idx].append(0)
            else:
                history_sequence[idx] = [
                    history_sequence[idx][0] + -1 * history_sequence[idx + 1][0]
                ] + history_sequence[idx]
                history_sequence[idx].append(
                    history_sequence[idx][-1] + history_sequence[idx + 1][-1]
                )

        return history_sequence

    def find_placeholders(self, part_two: bool = False):
        placeholders = [
            self.complete_history_sequence(history)[0][-1]
            if not part_two
            else self.complete_history_sequence(history)[0][0]
            for history in self.histories
        ]
        return placeholders


class TestMain(TestCase):
    def test_part1(self):
        test = Day09(f"{Path(__file__).parent}/test_input_part1.txt")
        self.assertEqual(test.find_placeholders(), [18, 28, 68])
        self.assertEqual(sum(test.find_placeholders()), 114)

    def test_part2(self):
        test = Day09(f"{Path(__file__).parent}/test_input_part1.txt")
        self.assertEqual(test.find_placeholders(True), [-3, 0, 5])
        self.assertEqual(sum(test.find_placeholders(True)), 2)


if __name__ == "__main__":
    solution = Day09(f"{Path(__file__).parent}/input.txt")
    print(sum(solution.find_placeholders()))
    print(sum(solution.find_placeholders(part_two=True)))
