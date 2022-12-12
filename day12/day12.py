#!/usr/bin/env python3
def read_input(in_file):
    """Read in the elevation map, replace start and end locations"""
    ht_map = []
    with open(in_file, "r") as f:
        for row, line in enumerate(f):

            if "S" in line:
                start_pos = (row, line.find("S"))
                line = line.replace("S", "a")
            if "E" in line:
                end_pos = (row, line.find("E"))
                line = line.replace("E", "z")

            ht_map.append(line.strip())

    return ht_map, start_pos, end_pos


def get_neighbours(ht_map, cur_pos, DIRS=[(-1, 0), (1, 0), (0, -1), (0, 1)]):
    """Get valid neighbors"""
    nbrs = []
    for dir in DIRS:
        new_pos = tuple(map(sum, zip(cur_pos, dir)))

        # Append to neighbours if valid
        if check_valid(ht_map, cur_pos, new_pos):
            nbrs.append(new_pos)

    return nbrs


def check_valid(ht_map, cur_pos, new_pos):
    """Check if new position is valid"""
    height, width = len(ht_map), len(ht_map[0])

    # If outside of map
    if not (0 <= new_pos[1] <= width - 1) or not (
        0 <= new_pos[0] <= height - 1
    ):
        return False

    # Check if adjacent position can be reached
    return (
        ord(ht_map[cur_pos[0]][cur_pos[1]])
        <= ord(ht_map[new_pos[0]][new_pos[1]]) + 1
    )


def move(ht_map, start_pos, end_pos, part):
    """Perform movements"""
    positions = [end_pos]
    visited = []
    steps = 0

    # Loop until starting position found (from end)
    while (
        (start_pos not in positions)
        if part == 1
        else ("a" not in [ht_map[pos[0]][pos[1]] for pos in positions])
    ):
        steps += 1
        new_positions = []
        # For each position, check neighbors
        for pos in positions:
            for nbrs in get_neighbours(ht_map, pos):
                if (
                    nbrs not in positions
                    and nbrs not in visited
                    and nbrs not in new_positions
                ):
                    new_positions.append(nbrs)
            visited.append(pos)
        positions = new_positions

    return steps


if __name__ == "__main__":
    # in_file = str(input("Enter the file containing the elevation map: "))
    in_file = "./input.txt"
    ht_map, start_pos, end_pos = read_input(in_file)

    # Part 1
    steps = move(ht_map, start_pos, end_pos, 1)
    print(f"Number of steps taken: {steps}")

    # Part 2
    steps = move(ht_map, start_pos, end_pos, 2)
    print(f"Number of steps taken: {steps}")
