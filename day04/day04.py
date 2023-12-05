#!/usr/bin/env python
from pathlib import Path
from unittest import TestCase


class Day04:
    def __init__(self, input: str):
        self.cards = self.load_cards(input)

    def load_cards(self, input: str) -> dict[str, dict[str, list[int]]]:
        cards: dict[str, dict[str, list[int]]] = {}

        with Path(input).open(encoding="utf-8") as in_file:
            for line in in_file:
                card, numbers = line.split(": ")
                win_nums, play_nums = numbers.strip().split(" | ")
                cards[card] = {
                    "Winning Numbers": [int(num) for num in win_nums.split()],
                    "Play Numbers": [int(num) for num in play_nums.split()],
                }

            return cards

    def find_cards(
        self, part_two: bool = False
    ) -> list[int]:  # pyright: ignore
        winning_cards: list[int] = [1] * len(self.cards) if part_two else []

        for cur_card, card in enumerate(self.cards):
            matching = len(
                set(self.cards[card]["Winning Numbers"])  # pyright: ignore
                & set(self.cards[card]["Play Numbers"])  # pyright: ignore
            )

            if not part_two:
                winning_cards.append(
                    2 ** (matching - 1) if matching > 0 else 0
                )
            else:
                for idx in range(cur_card + 1, cur_card + matching + 1):
                    winning_cards[idx] += winning_cards[cur_card]

        return winning_cards


class TestMain(TestCase):
    def test_part1(self):
        test = Day04(f"{Path(__file__).parent}/test_input_part1.txt")
        self.assertEqual(sum(test.find_cards()), 13)

    def test_part2(self):
        test = Day04(f"{Path(__file__).parent}/test_input_part2.txt")
        test_copies = test.find_cards(part_two=True)
        self.assertEqual(test_copies, [1, 2, 4, 8, 14, 1])
        self.assertEqual(sum(test_copies), 30)


if __name__ == "__main__":
    solution = Day04(f"{Path(__file__).parent}/input.txt")
    print(sum(solution.find_cards()))
    print(sum(solution.find_cards(part_two=True)))
