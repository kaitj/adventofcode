import os
import itertools


def find_missing(xmas_code, preamble):
    for line in range(0, len(xmas_code)):
        possible_sums = set(
            [sum(combo) for combo in itertools.combinations(xmas_code[line:line + preamble], 2)])

        if not xmas_code[preamble + line] in possible_sums:
            return xmas_code[line + preamble]

    return None


def find_weakness(xmas_code, missing_num):
    for line in range(0, len(xmas_code)):
        combo_sum = [combo for combo in itertools.accumulate(
            xmas_code[line:]) if combo <= missing_num][1:]

        if missing_num in combo_sum:
            index = combo_sum.index(missing_num)
            combo = xmas_code[line:][:index + 2]

            return min(combo) + max(combo)

    return None


def main():
    # User input
    xmas_file = input("Enter file containing XMAS-encrypted list: ")

    # Open file containing xmas code
    with open(os.path.realpath(xmas_file), "r") as in_file:
        xmas_code = in_file.read().split()
    xmas_code = list(map(int, xmas_code))

    # Part 1
    missing_num = find_missing(xmas_code, 25)
    print(f"First invalid number in XMAS-list is: {missing_num}")

    # Part 2
    weakness_sum = find_weakness(xmas_code, missing_num)
    print(f"The weakness in XMAS-list is: {weakness_sum}")


if __name__ == "__main__":
    main()
