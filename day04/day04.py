#!/usr/bin/env python3
def read_input(in_fpath):
    """Return assignments of pairs of elves"""
    with open(in_fpath, "r") as f:
        assignments = [assignment.strip().split(",") for assignment in f]

    return assignments


def overlap(assignment, part):
    """Determine whether elf pairs have overlapping assignment"""

    elf1_min, elf1_max = map(int, assignment[0].split("-"))
    elf2_min, elf2_max = map(int, assignment[1].split("-"))

    match part:
        case 1:
            if (elf1_min >= elf2_min and elf1_max <= elf2_max) or (
                elf2_min >= elf1_min and elf2_max <= elf1_max
            ):
                return 1
        case 2:
            if (elf1_min >= elf2_min and elf1_min <= elf2_max) or (
                elf2_min >= elf1_min and elf2_min <= elf1_max
            ):
                return 1

    return 0


if __name__ == "__main__":
    in_file = str(input("Enter path to elf assignments: "))
    assignments = read_input(in_file)

    # Part 1
    print(
        f"Fully overlapped assignments: {sum([overlap(assignment, 1) for assignment in assignments])}"
    )

    # Part
    print(
        f"Partial overlapped assignments: {sum([overlap(assignment, 2) for assignment in assignments])}"
    )
