#!/usr/bin/env python3
import json


def read_input(in_file):
    """Function to read input"""

    return open(in_file).read().strip()


def compare(a, b):
    """Helper to compare between ints / vals"""
    match (a, b):
        # Check left side smaller than right
        case int(), int():
            return b - a
        case list(), list():
            for aval, bval in zip(a, b):
                if (res := compare(aval, bval)) != 0:
                    return res
            return len(b) - len(a)
        # Casting both to same type
        case int(), list():
            return compare([a], b)
        case list(), int():
            return compare(a, [b])


def count_pairs(signals, part):
    """Count and sum number of valid pairs"""
    valid = 0
    decode_idx = [0, 0]
    for idx, signal_pair in enumerate(signals.split("\n\n")):
        signal = [
            json.loads(signal.strip()) for signal in signal_pair.split("\n")
        ]

        if compare(signal[0], signal[1]) > 0:
            valid += idx + 1

        for sig in signal:
            decode_idx[0] += 1 if compare(sig, [[2]]) > 0 else 0
            decode_idx[1] += 1 if compare(sig, [[6]]) > 0 else 0

    match part:
        case 1:
            return valid
        case 2:
            return (decode_idx[0] + 1) * (decode_idx[1] + 2)


if __name__ == "__main__":
    # in_file = str(input("Enter file containing distress signal: "))
    in_file = "./input.txt"
    signals = read_input(in_file)

    # Part 1
    print(f"Number of valid pairs: {count_pairs(signals, 1)}")

    # Part 2
    print(f"Product of decoder indices: {count_pairs(signals, 2)}")
