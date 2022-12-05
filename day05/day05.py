#!/usr/bin/env python3


def read_input(in_fpath):
    """Read and return drawing of stacks and instructions"""
    drawing, instructions = [
        line.split("\n") for line in open(in_fpath).read().split("\n\n")
    ]

    # Sort boxes into lists representing columns
    drawing = [
        [box for box in stack if box != " "][::-1]
        for stack in map(list, zip(*[*map(list, drawing)]))
        if stack[-1] != " "
    ]

    # Grab numerical values of instructions
    instructions = [
        [int(num) for num in line.split() if num.isdigit()]
        for line in instructions
        if line
    ]

    return drawing, instructions


def find_top(drawing, instructions, part):
    """Find box at top of stack"""

    for moves, old, new in instructions:
        match part:
            case 1:
                for _ in range(moves):
                    drawing[new - 1].append(drawing[old - 1].pop())
            case 2:
                drawing[new - 1].extend(drawing[old - 1][-moves:])
                del drawing[old - 1][-moves:]

    return "".join(map(lambda stack: stack[-1], drawing))


if __name__ == "__main__":
    in_file = str(input("Enter path containing drawing of stacks: "))

    # Part 1
    drawing, instructions = read_input(in_file)
    print(f"Top of each stack: {find_top(drawing, instructions, 1)}")

    # Part 2
    drawing, instructions = read_input(in_file)
    print(f"Top of each stack: {find_top(drawing, instructions, 2)}")
