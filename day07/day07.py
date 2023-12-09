#!/usr/bin/env python
from collections import Counter
from pathlib import Path
from unittest import TestCase

CARD_STRENGTH = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}

HAND_STRENGTH = {
    "high card": 0,
    "one pair": 1,
    "two pair": 2,
    "three of a kind": 3,
    "full house": 4,
    "four of a kind": 5,
    "five of a kind": 6,
}


class Day07:
    def __init__(self, input_path: str, part_two: bool = False):
        self.hands = self.load_hands(input_path, part_two)

    def load_hands(self, input_path: str, part_two: bool) -> list[tuple[str, int, str]]:
        hands: list[tuple[str, int, str]] = []
        with Path(input_path).open(encoding="utf-8") as in_file:
            for line in in_file:
                cards, bid = line.strip().split()
                hands.append(
                    (
                        cards,
                        int(bid),
                        self.determine_hands(cards, part_two),
                    )
                )

        return hands

    def determine_hands(self, hand: str, part_two: bool) -> str:
        """Determine hand and return strength"""
        card_count = Counter(hand)

        if part_two:
            CARD_STRENGTH["J"] = 0
            # If all "J"s, count as is
            if set(card_count.keys()) == {"J"}:
                pass
            # Otherwise, create best value (count each "J" separately)
            elif "J" in card_count:
                joker_count = card_count["J"]
                del card_count["J"]
                for _ in range(joker_count):
                    max_key = max(  # pyright: ignore
                        card_count, key=card_count.get  # pyright: ignore
                    )
                    card_count[max_key] += 1  # pyright: ignore

        for count in card_count.values():
            if count >= 4:
                return "five of a kind" if count == 5 else "four of a kind"

        if set(card_count.values()) == {2, 3}:
            return "full house"

        if 3 in card_count.values():
            return "three of a kind"

        if list(card_count.values()).count(2) == 2:
            return "two pair"

        if 2 in card_count.values():
            return "one pair"

        return "high card"

    def get_hand_keys(self, hand: tuple[str, int, str]) -> tuple[int, list[int]]:
        hand_key = HAND_STRENGTH.get(hand[2], -1)
        cards_key = [CARD_STRENGTH[card] for card in hand[0]]

        return hand_key, cards_key

    def sort_hands(self) -> list[tuple[str, int]]:
        return sorted(self.hands, key=self.get_hand_keys)  # pyright: ignore

    def total_winnings(self) -> int:
        sorted_hands = self.sort_hands()
        winnings = [hands[1] * rank for rank, hands in enumerate(sorted_hands, start=1)]

        return sum(winnings)


class TestMain(TestCase):
    def test_part1(self):
        test = Day07(f"{Path(__file__).parent}/test_input_part1.txt")
        self.assertEqual(test.total_winnings(), 6440)

    def test_part2(self):
        test = Day07(f"{Path(__file__).parent}/test_input_part2.txt", part_two=True)
        self.assertEqual(test.total_winnings(), 5905)


if __name__ == "__main__":
    solution = Day07(f"{Path(__file__).parent}/input.txt")
    print(solution.total_winnings())
    solution = Day07(f"{Path(__file__).parent}/input.txt", part_two=True)
    print(solution.total_winnings())
