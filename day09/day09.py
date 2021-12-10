from dataclasses import dataclass
from functools import reduce
from typing import Generator, Optional

import utils


@dataclass
class Location:
    """Location within of the height_map"""

    row: int
    col: int
    height: int

    @property
    def risk_level(self):
        return 1 + self.height

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.height == other.height
        return self.height == other

    def __lt__(self, other):
        if isinstance(other, Location):
            return self.height < other.height
        return self.height < other

    def __gt__(self, other):
        if isinstance(other, Location):
            return self.height > other.height
        return self.height > other

    def __hash__(self):
        return hash((self.row, self.col, self.height))


class HeightMap:
    """Height map containing locations"""

    def __init__(self, data: list[list[int]]):
        self.locations = [
            [Location(row, col, height) for col, height in enumerate(data[row])]
            for row in range(len(data))
        ]

    def __check_min_height(self, location: Location) -> bool:
        """Compare against adjacent locations to see if lowest"""
        above = (
            self[location.row - 1][location.col] if location.row > 0 else float("inf")
        )
        below = (
            self[location.row + 1][location.col]
            if location.row < len(self) - 1
            else float("inf")
        )
        left = (
            self[location.row][location.col - 1] if location.col > 0 else float("inf")
        )
        right = (
            self[location.row][location.col + 1]
            if location.col < len(self[location.row]) - 1
            else float("inf")
        )

        return self[location.row][location.col] < min(above, below, left, right)

    def __basin(
        self, location: Location, basin: Optional[set[Location]] = None
    ) -> set[Location]:
        """Identify basins by expanding until boundaries (9) is encountered"""
        basin = basin or set()

        if location in basin:
            return set()
        basin.add(location)

        # Up
        if location.row > 0 and self[location.row - 1][location.col] != 9:
            basin.update(self.__basin(self[location.row - 1][location.col], basin))

        # Down
        if location.row < len(self) - 1 and self[location.row + 1][location.col] != 9:
            basin.update(self.__basin(self[location.row + 1][location.col], basin))

        # Left
        if location.col > 0 and self[location.row][location.col - 1] != 9:
            basin.update(self.__basin(self[location.row][location.col - 1], basin))

        # Right
        if (
            location.col < len(self[location.row]) - 1
            and self[location.row][location.col + 1] != 9
        ):
            basin.update(self.__basin(self[location.row][location.col + 1], basin))

        return basin

    def low_locations(self) -> list[Location]:
        """Return locations of lowest height"""

        return [
            location
            for row in self
            for location in row
            if self.__check_min_height(location)
        ]

    def basins(self) -> Generator[set[Location], None, None]:
        for location in self.low_locations():
            yield self.__basin(location)

    def largest_basins(self, count: int = 3) -> Generator[set[Location], None, None]:
        return (basin for basin in sorted(self.basins(), key=len, reverse=True)[:count])

    def __getitem__(self, key):
        return self.locations[key]

    def __len__(self):
        return len(self.locations)

    def __iter__(self):
        for row in self.locations:
            yield row


def puzzle1(in_data: list[list[int]]):
    height_map = HeightMap(in_data)

    return sum(location.risk_level for location in height_map.low_locations())


def puzzle2(in_data: list[list[int]]):
    height_map = HeightMap(in_data)

    largest_basins = map(len, height_map.largest_basins(3))

    return reduce(lambda x, y: x * y, largest_basins)


if __name__ == "__main__":
    in_fpath = input("Enter height map file path: ")
    in_data = utils.parse_lines(in_fpath, int)

    # Puzzle 1
    print(f"The sum of the risk levels of all low points is: {puzzle1(in_data)}")

    # Puzzle 2
    print(f"The product of the 3 largest basins: {puzzle2(in_data)}")
