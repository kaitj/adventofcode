#!/usr/bin/env python3
DIR_TO_COORDS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def read_input(in_file):
    """Read and return map of tail visits"""
    move_map = []
    with open(in_file, "r") as f:
        for line in f:
            dir, steps = line.strip().split(" ")
            coords = DIR_TO_COORDS[dir]
            move_map.append((coords, int(steps)))

    return move_map


def move(head, tail):
    """Move head and tail positions"""
    dx, dy = head[0] - tail[0], head[1] - tail[1]
    x_dist, y_dist = abs(dx), abs(dy)

    # Determine if head and tail are touching
    max_dist = max(x_dist, y_dist)
    if max_dist <= 1:
        return tail

    # Determine movement to be added to tail
    x_cor = (1 if dx >= 0 else -1) * min(x_dist, 1)
    y_cor = (1 if dy >= 0 else -1) * min(y_dist, 1)

    return tail[0] + x_cor, tail[1] + y_cor


def find_tail_visits(moves, num_tails=1):
    """Determine the number of tail positions"""
    pos = (0, 0)
    tails = [pos for _ in range(num_tails)]

    visited = set()
    for (dx, dy), steps in moves:
        for _ in range(steps):
            pos = pos[0] + dx, pos[1] + dy
            head = pos

            for i in range(num_tails):
                tails[i] = move(head, tails[i])
                head = tails[i]
            visited.add(tails[-1])

    return len(visited)


if __name__ == "__main__":
    in_file = str(input("Enter the path to the movement map: "))
    move_map = read_input(in_file)

    # Part 1
    print(
        f"The number of locations the tail has visited: {find_tail_visits(move_map)}"
    )

    # Part 2
    print(
        f"The number of locations the tail has visited: {find_tail_visits(move_map, 9)}"
    )
