#!/usr/bin/env python3
shapes = {"A": "X", "B": "Y", "C": "Z"}
scores = {"X": 1, "Y": 2, "Z": 3}
win = {"Y": "X", "Z": "Y", "X": "Z"}
lose = {val: key for key, val in win.items()}


def read_input(in_fpath):
    """Read strategy into dictionary"""
    strategy = []
    with open(in_fpath, "r") as f:
        for line in f:
            opp, play = line.strip().split(" ")
            strategy.append((opp, play))

    return strategy


def calc_score(strategy, part):
    """Calculate total score of game"""
    total = 0

    for opp, play in strategy:
        match part:
            case 1:
                total += scores[play]
                if shapes[opp] == play:
                    total += 3
                elif win[play] == shapes[opp]:
                    total += 6

            case 2:
                match play:
                    case "Y":
                        total += 3 + scores[shapes[opp]]
                    case "Z":
                        total += 6 + scores[lose[shapes[opp]]]
                    case "X":
                        total += scores[win[shapes[opp]]]

    return total


if __name__ == "__main__":
    # Read input
    in_fpath = str(input("Enter the path to the strategy guide: "))
    strategy = read_input(in_fpath)

    # Part 1
    print(f"Answer to part 1: {calc_score(strategy, 1)}")

    # # Part 2
    print(f"Answer to part 2: {calc_score(strategy, 2)}")
