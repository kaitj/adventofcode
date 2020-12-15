# "." - open square; "#" - tree
import os
import numpy as np


def find_trees(hill, slope):
    trees = 0
    position = 0

    for row in range(0, len(hill), slope[1]):
        trees += (hill[row][position % (len(hill[0]) - 1)] == '#')
        position += slope[0]

    return trees


def main():
    # Input
    input_map = input("Enter the path containing to the input map: ")

    # Read map
    with open(os.path.realpath(input_map), "r") as input_file:
        hill = input_file.readlines()

    # Part 1
    trees = find_trees(hill, [3, 1])
    print("Number of trees encountered on path in part 1: {}".format(trees))

    # Part 2
    trees = np.product([find_trees(hill, [1, 1]),
                        find_trees(hill, [3, 1]),
                        find_trees(hill, [5, 1]),
                        find_trees(hill, [7, 1]),
                        find_trees(hill, [1, 2])])
    print("Number of trees encountered on path in part 2: {}".format(trees))


if __name__ == "__main__":
    main()
