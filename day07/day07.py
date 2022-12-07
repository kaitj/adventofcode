#!/usr/bin/env python3
from bisect import bisect_right
from collections import Counter
from pathlib import Path


def analyze_output(term_out):
    """Read terminal input and analyze directory sizes"""
    dir_sizes = Counter()  # Keep track of directory sizes

    with open(term_out, "r") as f:
        for line in f:
            args = line.strip().split()

            # If command
            if args[0] == "$":
                if args[1] == "cd":
                    if args[2] == "/":
                        currdir = Path("/")
                    elif args[2] == "..":
                        currdir = currdir.parent
                    else:
                        currdir = currdir.joinpath(args[2])
            # If checking directory
            elif args[0] != "dir":
                # Add size to current directory
                dir_sizes[currdir] += (size := int(args[0]))

                # Also add size parent directories
                for parent in currdir.parents:
                    dir_sizes[parent] += size

    return dir_sizes


def find_dirs(dir_sizes, part):
    sorted_dirs = sorted(dir_sizes.values())
    match part:
        case 1:
            return sum(
                dir_size for dir_size in sorted_dirs if dir_size <= 100000
            )
        case 2:
            # Use bisect to find index of folder to be deleted to find size
            return sorted_dirs[
                bisect_right(sorted_dirs, dir_sizes[Path("/")] - 40000000)
            ]


if __name__ == "__main__":
    term_out = str(input("Enter file containing terminal output: "))

    # Determine directory sizes
    dir_sizes = analyze_output(term_out)

    # Part 1
    print(f"Total size of directories <= 100,000: {find_dirs(dir_sizes, 1)}")

    # Part 2
    print(f"Size of directory to be deleted: {find_dirs(dir_sizes, 2)}")
