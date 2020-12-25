import os
import operator
from functools import reduce


def parse_file(input_file):
    tiles = {}

    # Extract tile info
    with open(os.path.realpath(input_file), "r") as in_file:
        all_tiles = in_file.read()
    all_tiles = all_tiles.rsplit("\n\n")

    for info in all_tiles:
        tile_id, tile_map = info.split(":\n")
        tile_id = int(tile_id[5:])
        tiles[tile_id] = tile_map.split("\n")

    return tiles


def flip(tile):
    return [row[::-1] for row in tile]


def rotate(tile):
    return ["".join(row[::-1]) for row in zip(*tile)]


def tile_transforms(tile):
    tile90 = rotate(tile)
    tile180 = rotate(tile90)
    tile270 = rotate(tile180)

    return [tile, tile90, tile180, tile270, flip(
        tile), flip(tile90), flip(tile180), flip(tile270)]


def form_image(transformed_tiles):
    width = int(len(transformed_tiles)**0.5)
    assembled = [[(0, 0)] * width for _ in range(width)]
    unsolved_tiles = set(transformed_tiles.keys())

    def _find_tile(coordinates):
        if coordinates == width**2:
            return True
        row, col = coordinates // width, coordinates % width

        for tile_id in list(unsolved_tiles):
            for idx, transform in enumerate(transformed_tiles[tile_id]):
                # Set flags to check edges
                up_flag = left_flag = True
                if row > 0:
                    up_tile_id, up_transform = assembled[row - 1][col]
                    up_tile = transformed_tiles[up_tile_id][up_transform]
                    up_flag = all(transform[0][idx] == up_tile[-1][idx]
                                  for idx in range(len(up_tile[-1])))

                if col > 0:
                    left_tile_id, left_transform = assembled[row][col - 1]
                    left_tile = transformed_tiles[left_tile_id][left_transform]
                    left_flag = all(transform[idx][0] == left_tile[idx][-1]
                                    for idx in range(len(left_tile[-1])))

                if up_flag and left_flag:
                    assembled[row][col] = (tile_id, idx)
                    unsolved_tiles.remove(tile_id)

                    if _find_tile(coordinates + 1):
                        return True

                    unsolved_tiles.add(tile_id)

        return False

    _find_tile(0)

    return assembled


def monster_idx():
    monster_pattern = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
    ]

    return [(row, col) for row in range(len(monster_pattern))
            for col in range(len(monster_pattern[row]))
            if monster_pattern[row][col] == "#"]


def find_monster(image, transformed_tiles):
    # Remove image border and gaps
    width = int(len(transformed_tiles)**0.5)
    borderless_img = [["."] * (width * (len(transformed_tiles) - 1))
                      for _ in range(width * (len(transformed_tiles) - 1))]

    for row in range(width):
        for col in range(width):
            tile_id, transform = image[row][col]
            tile = transformed_tiles[tile_id][transform]
            for row2 in range(1, len(transformed_tiles[tile_id][0][0]) - 1):
                for col2 in range(1, len(
                        transformed_tiles[tile_id][0][0]) - 1):
                    borderless_img[8 * row + row2 - 1]\
                        [8 * col + col2 - 1] = tile[row2][col2]

    for img in tile_transforms(borderless_img):
        monster = 0
        for row in range(len(img) - 3):
            for col in range(len(img) - 20):
                if all(img[row + delta_row][col + delta_col] ==
                       "#" for delta_row, delta_col in monster_idx()):
                    monster += 1

        # Count water roughness:
        if monster > 0:
            roughness = sum(row.count("#") for row in img)
            return roughness - monster * len(monster_idx())


def main():
    # Read in tile information
    tiles = parse_file(input("Entire file containing tiles: "))
    transformed_tiles = {
        tile_id: tile_transforms(tile_map) for tile_id,
        tile_map in tiles.items()}

    # Form image
    image = form_image(transformed_tiles)

    # Part 1
    prod_cornerids = reduce(operator.mul,
                            [image[0][0][0],
                             image[0][-1][0],
                             image[-1][0][0],
                             image[-1][-1][0]])
    print(f"The product of the corner ids is: {prod_cornerids}")

    # Part 2
    print(find_monster(image, transformed_tiles))


if __name__ == "__main__":
    main()
