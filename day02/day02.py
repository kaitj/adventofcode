#!/usr/bin/env python
import re
from pathlib import Path

from aoc.utils import day_parser


class Day02:
    def __init__(self, input: str):
        self.total_cubes = {"red": 12, "green": 13, "blue": 14}
        self.games = self.load_games(input)

    def load_games(self, input: str) -> dict[int, dict[str, list[int]]]:
        games: dict[int, dict[str, list[int]]] = {}
        with open(input, "r", encoding="utf-8") as in_file:
            for line in in_file:
                game, record = line.split(": ")
                game = int(game.split(" ")[-1])
                games[game] = {
                    colour: [int(val) for val in re.findall(rf"(\d+) {colour}", record)]
                    for colour in self.total_cubes.keys()
                }

            return games

    def find_valid_games(self) -> list[int]:
        valid_games = [game for game in self.games.keys() if self.is_valid_game(game)]
        return valid_games

    def is_valid_game(self, game: int) -> bool:
        return all(
            max(self.games[game][colour]) <= self.total_cubes[colour]
            for colour in self.total_cubes.keys()
        )

    def find_game_power(self) -> list[int]:
        power = [
            max(self.games[game]["red"])
            * max(self.games[game]["blue"])
            * max(self.games[game]["green"])
            for game in self.games.keys()
        ]
        return power


class TestMain:
    def test_part1(self):
        test = Day02(f"{Path(__file__).parent}/test_input_part1.txt")
        assert sum(test.find_valid_games()) == 8

    def test_part2(self):
        test = Day02(f"{Path(__file__).parent}/test_input_part2.txt")
        assert sum(test.find_game_power()) == 2286


def main():
    args = day_parser().parse_args()

    solution = Day02(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(sum(solution.find_valid_games()))
    elif args.part == 2:
        print(sum(solution.find_game_power()))
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
