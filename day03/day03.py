#!/usr/bin/env python3
from itertools import islice


def read_input(in_fpath, part):
    """Read rucksack lines"""
    rucksack = []
    with open(in_fpath, "r") as f:
        match part:
            case 1:
                for line in f:
                    line = line.strip()
                    n = len(line)
                    rucksack.append((line[: n // 2], line[n // 2 :]))
            case 2:
                while True:
                    lines = list(islice(f, 3))
                    if not lines:
                        break
                    lines = [line.strip() for line in lines]
                    rucksack.append(lines)

    return rucksack


def common(compartment, part):
    """Find common element and return priority"""
    match part:
        case 1:
            letter = next(iter(set(compartment[0]) & set(compartment[1])))
        case 2:
            letter = next(
                iter(
                    (set(compartment[0]) & set(compartment[1]))
                    & set(compartment[2])
                )
            )

    if letter.islower():
        return ord(letter) - 96
    else:
        return ord(letter) - 38


def priority_sum(rucksack, part):
    """Compute sum of priorities"""
    return sum([common(compartment, part) for compartment in rucksack])


if __name__ == "__main__":
    in_file = str(input("Enter path to file: "))

    # Part 1
    rucksack = read_input(in_file, 1)
    print(f"Sum of priorities is: {priority_sum(rucksack, 1)}")

    # Part 2
    rucksack = read_input(in_file, 2)
    print(f"Sum of priorities is: {priority_sum(rucksack, 2)}")
