#!/usr/bin/env python
import re


def read_input(in_file):
    """Read input file"""
    positions = {"S": [], "B": []}

    with open(in_file, "r") as f:
        for line in f:
            line_pos = list(map(int, re.findall("(-?\d+)", line)))
            positions["S"].append((line_pos[0], line_pos[1]))
            positions["B"].append((line_pos[2], line_pos[3]))

    return positions


def no_beacon_pos(positions, row):
    """Find number of positions that cannot contain a beacon"""
    beacons, non_beacons = set(positions["B"]), set()

    for idx in range(len(positions["B"])):
        sx, sy = positions["S"][idx][0], positions["S"][idx][1]
        bx, by = positions["B"][idx][0], positions["B"][idx][1]

        # Find non-beacon positions
        res = abs(sx - bx) + abs(sy - by)
        res_y = abs(sy - row)
        max_res_x = res - res_y
        if max_res_x >= 0:
            for dx in range(-max_res_x, max_res_x + 1):
                non_beacons.add((sx + dx, row))

    return len(non_beacons - beacons)


def beacon_ranges(positions, row):
    non_beacons = set()

    for idx in range(len(positions["B"])):
        sx, sy = positions["S"][idx][0], positions["S"][idx][1]
        bx, by = positions["B"][idx][0], positions["B"][idx][1]

        # Find positions
        res = abs(sx - bx) + abs(sy - by)
        res_y = abs(sy - row)
        max_res_x = res - res_y
        if max_res_x >= 0:
            min_x, max_x = sx - max_res_x, sx + max_res_x
            if max_x >= min_x:
                non_beacons.add((min_x, max_x))

    return non_beacons


def find_freq(positions, MUL=4_000_000):
    x_range, y_range = (0, 4_000_000 + 1), (0, 4_000_000 + 1)

    for row in range(*y_range):
        non_beacons = beacon_ranges(positions, row)
        non_beacons |= set((bx, bx) for bx, by in positions["B"] if by == row)

        last_x = x_range[0]

        for res in sorted(non_beacons):
            min_x, max_x = res
            if last_x < min_x:
                return last_x * MUL + row
            if max_x >= last_x:
                last_x = max_x + 1

        if last_x <= x_range[1]:
            return last_x * MUL + row


if __name__ == "__main__":
    in_file = str(input("Enter file containing sensor and beacon positions: "))
    pos = read_input(in_file)

    # Part 1
    print(f"Number of non-beacon positions: {no_beacon_pos(pos, 10)}")

    # Part 2
    print(f"Tuning frequency: {find_freq(pos)}")
