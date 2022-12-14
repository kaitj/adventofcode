#!/usr/bin/env python3
material = {
    "rock": "#",
    "air": ".",
    "sand": "o",
}


def create_map(in_file):
    """Read input file and create map"""
    bottom_rock = 0
    cave = {}

    with open(in_file, "r") as f:
        for line in f:
            coords = [
                tuple(map(int, coord.split(",")))
                for coord in line.strip().split(" -> ")
            ]

            for idx in range(len(coords) - 1):
                x1, y1 = coords[idx][0], coords[idx][1]
                x2, y2 = coords[idx + 1][0], coords[idx + 1][1]

                # # Find bottom rock
                bottom_rock = max(y1, y2, bottom_rock)

                # Map out rocks
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    for x in range(min(x1, x2), max(x1, x2) + 1):
                        cave[x, y] = material["rock"]

    return cave, bottom_rock


def count_sand(cave_map, bottom_rock, part):
    grains = 0
    rest_grains = 0
    floor = bottom_rock + 2
    sand_coord = None
    while sand_coord != (500, 0):
        sand_coord = (500, 0)

        # Simulate sand falling
        while True:
            y = sand_coord[1] + 1
            for dx in [0, -1, 1]:
                x = sand_coord[0] + dx

                if (
                    y < floor
                    and cave_map.get((x, y), material["air"])
                    == material["air"]
                ):
                    sand_coord = (x, y)
                    break
            else:
                if not rest_grains and sand_coord[1] > bottom_rock:
                    rest_grains = grains
                cave_map[sand_coord] = material["sand"]
                break
        grains += 1

    match part:
        case 1:
            return rest_grains
        case 2:
            return grains


if __name__ == "__main__":
    # Read input
    in_file = str(input("Enter file containing rock map: "))

    # Part 1
    cave_map, bottom_rock = create_map(in_file)
    print(
        f"Number of grains come to rest: {count_sand(cave_map, bottom_rock, 1)}"
    )

    # Part 2
    cave_map, bottom_rock = create_map(in_file)
    print(
        f"Number of grains until blocked: {count_sand(cave_map, bottom_rock, 2)}"
    )
