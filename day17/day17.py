import os
from typing import NamedTuple
from itertools import product
from collections import Counter


class Coord(NamedTuple):
    x: int
    y: int
    z: int = 0
    w: int = 0

    def __add__(self, others):
        # Add coordinates together
        return Coord(*(vec1 + vec2 for vec1, vec2 in zip(self, others)))


def get_surrounding(ndims):
    # Get all possible surrounding coordinates
    return {Coord(*col)
            for col in product(range(-1, 2), repeat=ndims)} - {Coord(0, 0)}


def update_cube(actives, surrounding):
    # Count number of active neighbours
    num_neighbours = Counter(
        active + surround for active in actives for surround in surrounding)
    # Identify newly active cubes in next state
    next_active = {
        coords for coords,
        neighbours in num_neighbours.items() if neighbours == 3} - actives
    # Identify cubes which survive from current state
    next_active |= {
        coords for coords in actives if num_neighbours[coords] in {
            2, 3}}

    return next_active


def main():
    cube_file = input("Enter file containing the slice of the 3D cube: ")

    # Identify where actives exist on cube slice
    with open(os.path.realpath(cube_file), "r") as in_file:
        actives = {Coord(x, y) for y, row in enumerate(in_file)
                   for x, col in enumerate(row) if col == "#"}

    # Get surrounding neighbours
    surrounding_p1 = get_surrounding(3)
    surrounding_p2 = get_surrounding(4)

    # Loop through iterations
    actives_p1 = actives_p2 = actives
    for _ in range(6):
        actives_p1 = update_cube(actives_p1, surrounding_p1)
        actives_p2 = update_cube(actives_p2, surrounding_p2)

    print("Part 1: The number of cubes in an active"
          f" state after sixth cycle is: {len(actives_p1)}")
    print("Part 2: The number of cubes in an active"
          f" state after sixth cycle is: {len(actives_p2)}")


if __name__ == '__main__':
    main()
