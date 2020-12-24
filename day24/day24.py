import os
import re
from collections import defaultdict, Counter


TILES_COORDS = {"e": (2, 0), "se": (1, -1), "sw": (-1, -1),
                "w": (-2, 0), "nw": (-1, 1), "ne": (1, 1)}


def identify_tile(instruction):
    position = (0, 0)

    for direction in instruction:
        position = tuple(map(sum, zip(position, TILES_COORDS[direction])))

    return position


def sim_days(tiles, days):
    for _ in range(days):
        tiles_counter = Counter(
            neighbour for coords in tiles for neighbour in neighbours(coords))

        tiles = set(coords for coords, neighbour_tiles in tiles_counter.items()
                    if ((coords in tiles and not (neighbour_tiles == 0 or
                                                  neighbour_tiles > 2)) or
                        (coords not in tiles and neighbour_tiles == 2)
                        )
                    )

    return tiles


def neighbours(coords):
    for change in TILES_COORDS.values():
        yield tuple(map(sum, zip(coords, change)))


def main():
    # Read instructions file
    dir_file = input("Enter file containing directional instructions: ")

    dir_reg = re.compile(r"e|se|sw|w|nw|ne")
    with open(os.path.realpath(dir_file), "r") as in_file:
        instructions = [dir_reg.findall(line.strip()) for line in in_file]

    # Set up boolean dictionary to determine flip
    tiles = defaultdict(bool)

    for instruction in instructions:
        position = identify_tile(instruction)
        # True = flipped to black
        tiles[position] = not tiles[position]
    tiles = set(filter(tiles.get, tiles))

    # Part 1
    blk_tiles = len(tiles)
    print(f"Number of black tiles after flips are: {blk_tiles}")

    # Part 2
    tiles = sim_days(tiles, 100)
    print(f"Number of black tiles after 100 days: {len(tiles)}")


if __name__ == "__main__":
    main()
