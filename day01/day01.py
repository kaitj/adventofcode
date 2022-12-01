#!/usr/bin/env python3
def read_input(in_fpath: str) -> list[list[int]]:
    """Read input and separate by elves"""
    with open(in_fpath, "r") as f:
        # Seperate by elves
        elves = f.read().strip().split("\n\n")
        elves = [list(map(int, elf.split("\n"))) for elf in elves]

    return elves


def calories(elves: list[list[int]], part: int) -> int:
    """Return number of calories as defined by question part"""
    calories = [sum(elf) for elf in elves]
    match part:
        case 1:
            return max(calories)
        case 2:
            return sum(sorted(calories, reverse=True)[:3])


if __name__ == "__main__":
    in_file = str(input("Enter path to file: "))
    elf_calories = read_input(in_file)

    # Part 1
    print(f"Answer to part 1: {calories(elf_calories, part=1)}")

    # Part 2
    print(f"Answer to part 1: {calories(elf_calories, part=2)}")
