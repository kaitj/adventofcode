#!/usr/bin/env python3
def read_input(in_fpath):
    """Read in datastream buffer"""
    with open(in_fpath, "r") as f:
        data = f.read().strip()

    return data


def packet_detect(data, part):
    """Determine when packet is first detected"""
    for i in range(len(data)):
        if part == 1 and len(set(data[i : i + 4])) == 4:
            return i + 4

        if part == 2 and len(set(data[i : i + 14])) == 14:
            return i + 14


if __name__ == "__main__":
    in_file = str(input("Enter file containing incoming datastream: "))
    data = read_input(in_file)

    # Part 1
    marker = packet_detect(data, 1)
    print(
        f"The number of characters processed before start-of-packet: {marker}"
    )

    # Part 2
    marker = packet_detect(data, 2)
    print(
        f"The number of characters processed before start-of-message: {marker}"
    )
