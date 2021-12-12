from collections import defaultdict, deque

import utils


def create_adjacency(paths: list) -> dict:
    adjacency_list = defaultdict(list)

    for line in paths:
        loc1, loc2 = line.split("-")
        adjacency_list[loc1].append(loc2)
        adjacency_list[loc2].append(loc1)

    return adjacency_list


def resolve_paths(adjacency: defaultdict(list), visit_twice: bool = False) -> int:
    # Current position, small caves, if small cave traversed twice (pt 2)
    start_path = ("start", set(["start"]), None)
    path_queue = deque([start_path])
    num_resolved = 0

    while path_queue:
        position, small, twice = path_queue.popleft()

        # Check if end of cave
        if position == "end":
            num_resolved += 1
            continue

        for loc in adjacency[position]:
            # Check if cave is small and already traversed
            if loc not in small:
                small_caves = set(small)
                # Add to traversed caves
                if loc.lower() == loc:
                    small_caves.add(loc)
                path_queue.append((loc, small_caves, twice))
            elif (
                loc in small
                and loc not in ["start", "end"]
                and twice is None
                and visit_twice
            ):
                path_queue.append((loc, small, loc))

    return num_resolved


def puzzle(data: str, visit_twice: bool = False) -> int:
    adjacency = create_adjacency(data)

    return resolve_paths(adjacency, visit_twice)


if __name__ == "__main__":
    in_fpath = input("Enter file containing possible paths: ")
    in_data = utils.parse_lines(in_fpath)

    # Puzzle 1
    print(f"Number of possible paths: {puzzle(in_data)}")

    # Puzzle 1
    print(f"Number of possible paths: {puzzle(in_data, True)}")
