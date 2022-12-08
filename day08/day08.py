#!/usr/bin/env python3
def read_input(in_file):
    """Read and return nested list containing tree map"""
    with open(in_file, "r") as f:
        tree_map = [[int(num) for num in line.strip()] for line in f]

    return tree_map


def is_visible(tree_map, map_height, map_width, row, col):
    """Determine if a given tree is visible"""
    cur_tree_height = tree_map[row][col]
    coords = (row, col)

    visible_out, score = False, 1
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        row, col = coords
        visible = 0

        while 0 < col < map_width - 1 and 0 < row < map_height - 1:
            visible += 1

            if tree_map[row + dy][col + dx] >= cur_tree_height:
                break

            row += dy
            col += dx

        # Determine whether tree is visible from outside
        if (
            row <= 0 or 
            row >= map_height - 1 or 
            col <= 0 or 
            col >= map_width - 1
        ):
            visible_out = True

        # Determine scenic score
        score *= visible

    return visible_out, score


def visible_trees(tree_map, part):
    """Search trees and determine number of visible trees"""
    map_height, map_width = len(tree_map), len(tree_map[0])

    trees_visible, max_scenic_score = 0, 0

    for row in range(map_height):
        for col in range(map_width):
            visible_out, scenic_score = is_visible(
                tree_map, map_height, map_width, row, col
            )
            trees_visible += visible_out

            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    match part:
        case 1:
            return trees_visible
        case 2:
            return max_scenic_score


if __name__ == "__main__":
    in_file = str(input("Enter the file containing the tree mapping: "))
    tree_map = read_input(in_file)

    # Part 1
    print(
        f"Number of visible trees from outside: {visible_trees(tree_map, 1)}"
    )

    # Part 2
    print(f"Maximum scenic score: {visible_trees(tree_map, 2)}")
