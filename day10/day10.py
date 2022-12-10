#!/usr/bin/env python3
CMD_TO_CYCLE = {"noop": 1, "addx": 2}


def read_input(in_file):
    """Read program and return commands"""

    out = []
    with open(in_file, "r") as f:
        for line in f:
            line = line.strip()

            if line == "noop":
                out.append((line, 0))
            else:
                out.append(tuple(line.split(" ")))

    return out


def signal_strength(program):
    """Run program and return signal strength"""
    X, cycle = 1, 0
    signal_strength = 0

    for cmd, val in program:
        for _ in range(CMD_TO_CYCLE[cmd]):
            if abs(X - (cycle % 40)) <= 1:
                print("#", end="")
            else:
                print("_", end="")
            cycle += 1
            # Start new line if end of line reached
            if cycle % 40 == 0:
                print()

            if cycle == 20 or (cycle - 20) % 40 == 0:
                signal_strength += X * cycle

        X += int(val)

    return signal_strength


def draw(cycle, X):
    n = cycle % 40
    if abs(X - n) <= 1:
        print("#", end="")
    else:
        print(".", end="")

    if cycle > 0 and n == 0:
        print()


if __name__ == "__main__":
    in_file = str(input("Enter file containing program: "))
    program = read_input(in_file)

    # Part 1
    print(f"\n\nSignal strength: {signal_strength(program)}")
