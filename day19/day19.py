import itertools as it
import re
from collections import defaultdict, deque
from copy import copy
from pathlib import Path
from typing import Self

OVERLAP_THRESHOLD = 11
ROTATIONS = 24


class Scanner:
    def __init__(self: Self, id: int):
        self.id = id
        self.beacons = None
        self.vectors = None

    def __repr__(self: Self) -> str:
        return f"Scanner {self.id}"

    def find_vectors_between_beacons(self: Self) -> None:
        def find_vector(
            this: tuple[int, ...], other: tuple[int, ...]
        ) -> tuple[int, ...]:
            x1, y1, z1 = this
            x2, y2, z2 = other

            return ((x2 - x1), (y2 - y1), (z2 - z1))

        vectors: dict[tuple[int, ...], set[tuple[int, ...]]] = defaultdict(set)  # type: ignore
        for one, other in it.combinations(self.beacons, 2):  # type: ignore
            vectors[one].add(find_vector(one, other))  # type: ignore
            vectors[other].add(find_vector(other, one))  # type: ignore

        self.vectors = vectors  # type: ignore

    def rotate(self: Self, i: int) -> None:
        def rotations(beacon: tuple[int, ...], i: int) -> tuple[int, int, int]:
            x, y, z = beacon
            rotates = [
                (x, y, z),
                (z, y, -x),
                (-x, y, -z),
                (-z, y, x),
                (-x, -y, z),
                (-z, -y, -x),
                (x, -y, -z),
                (z, -y, x),
                (x, -z, y),
                (y, -z, -x),
                (-x, -z, -y),
                (-y, -z, x),
                (x, z, -y),
                (-y, z, -x),
                (-x, z, y),
                (y, z, x),
                (z, x, y),
                (y, x, -z),
                (-z, x, -y),
                (-y, x, z),
                (-z, -x, y),
                (y, -x, z),
                (z, -x, -y),
                (-y, -x, -z),
            ]
            return rotates[i]

        new_beacons = [rotations(beacon, i) for beacon in self.beacons]
        self.beacons = new_beacons
        self.find_vectors_between_beacons()


def parse_input(in_fpath: Path) -> list[Scanner]:
    regex = r"--- scanner (\d+) ---"
    scanners: list[Scanner] = []
    beacons: list[tuple[int, ...]] = []
    current = None

    with in_fpath.open() as in_file:
        for line in in_file:
            is_new_scanner = re.findall(regex, line.strip())

            if is_new_scanner:
                if current:
                    current.beacons = beacons  # type: ignore
                    beacons = []

                new_scanner = Scanner(int(is_new_scanner[0]))
                scanners.append(new_scanner)
                current = new_scanner

            elif line and line.strip():
                beacon = tuple(map(int, line.strip().split(",")))
                beacons.append(beacon)

        current.beacons = beacons  # type: ignore

        for scanner in scanners:
            scanner.find_vectors_between_beacons()

    return scanners


def find_overlaps(this_scanner: Scanner, other_scanner: Scanner) -> defaultdict:
    overlaps = defaultdict(set)
    beacon_pairs = it.product(this_scanner.beacons, other_scanner.beacons)

    for this_beacon, other_beacon in beacon_pairs:
        v_this = this_scanner.vectors[this_beacon]
        v_other = other_scanner.vectors[other_beacon]
        overl = len(v_this & v_other)
        if overl >= OVERLAP_THRESHOLD:
            overlaps[this_beacon].add(other_beacon)

    return overlaps


def find_and_normalize(scanners: deque, debug=False) -> tuple:
    anchor = scanners.popleft()
    scanner_coords = {}

    while scanners:
        tested_scanner = scanners.popleft()
        offset = False
        overlap_found = False

        if debug:
            print(
                f"Testing anchor ({anchor}) with {len(anchor.beacons)} beacons against {tested_scanner}..."
            )

        for i in range(ROTATIONS):
            rotated_scanner = copy(tested_scanner)
            rotated_scanner.rotate(i)
            overlaps = find_overlaps(anchor, rotated_scanner)

            if overlaps:
                overlap_found = True
                this_beacon = list(overlaps.keys())[0]
                other_beacon = overlaps[this_beacon].pop()
                offset = (
                    this_beacon[0] - other_beacon[0],
                    this_beacon[1] - other_beacon[1],
                    this_beacon[2] - other_beacon[2],
                )

                scanner_coords[rotated_scanner.id] = offset

                new_beacons = []
                for beacon in rotated_scanner.beacons:
                    x, y, z = beacon
                    ox, oy, oz = offset
                    offset_beacon = (x + ox, y + oy, z + oz)
                    new_beacons.append(offset_beacon)

                anchor.beacons = list(set(anchor.beacons + new_beacons))
                anchor.find_vectors_between_beacons()

                if debug:
                    print(f"Merged! Anchor now has {len(anchor.beacons)} beacons.")

                break

        if not overlap_found:
            scanners.append(tested_scanner)

    return len(set(anchor.beacons)), scanner_coords


def manhattan(this_scanner_coords: tuple, other_scanner_coords: tuple) -> int:
    x1, y1, z1 = this_scanner_coords
    x2, y2, z2 = other_scanner_coords
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def find_max_distance(scanner_coords: dict) -> int:
    max_dist = 0
    for this, other in it.product(scanner_coords, repeat=2):
        dist = manhattan(this, other)
        if dist > max_dist:
            max_dist = dist
    return max_dist


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    scanners = deque(parse_input(in_fpath))
    unique_beacons, scanner_coords = find_and_normalize(scanners)

    print(f"Answer: {unique_beacons}")
    print(f"Answer: {find_max_distance(scanner_coords.values())}")
