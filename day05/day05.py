#!/usr/bin/env python
from pathlib import Path
from unittest import TestCase


class Day05:
    def __init__(self, input: str, part_two: bool = False) -> None:
        self.almanac = self.load_almanac(input=input, part_two=part_two)

    def load_almanac(
        self, input: str, part_two: bool
    ) -> dict[str, tuple[int] | list[tuple[int, int]]]:
        """
        seeds - locations
        maps - seed start, source start, range length
          -> if not mapped, seed = soil
        """
        almanac: dict[str, tuple[int] | set[int] | list[tuple[int]]] = {}

        with Path(input).open(encoding="utf-8") as in_file:
            almanac_lines = in_file.read().split("\n\n")

            seed_ranges = tuple(  # pyright: ignore
                map(int, almanac_lines[0].split(":")[1].split())
            )
            if part_two:
                # Handle seed ranges
                almanac["seeds"] = [  # pyright: ignore
                    (start, start + length)
                    for start, length in zip(
                        seed_ranges[::2], seed_ranges[1::2]
                    )
                ]
            else:
                almanac["seeds"] = seed_ranges  # pyright: ignore

            for almanac_line in almanac_lines[1:]:
                map_type, mapping = almanac_line.split(":")
                almanac[
                    map_type.strip().replace(" map", "")  # pyright: ignore
                ] = [
                    tuple(map(int, entry.split()))
                    for entry in mapping.lstrip().strip().split("\n")
                ]

        return almanac  # pyright: ignore

    def _find_overlap(
        self, rnge1: tuple[int, int], rnge2: tuple[int, int]
    ) -> tuple[int, int] | None:
        rnge1_start, rnge1_end = rnge1
        rnge2_start, rnge2_end = rnge2

        overlap_start = max(rnge1_start, rnge2_start)
        overlap_end = min(rnge1_end, rnge2_end)

        return (
            (overlap_start, overlap_end)
            if overlap_start <= overlap_end
            else None
        )

    def _shift_range(
        self, rnge: tuple[int, int], length: int
    ) -> tuple[int, int]:
        range_start, range_end = rnge
        return (range_start + length, range_end + length)  # pyright: ignore

    def _split_range(
        self, rnge: tuple[int, int], overlap: tuple[int, int]
    ) -> set[tuple[int, int]]:
        result: set[tuple[int, int]] = set()

        overlap_start, overlap_end = overlap
        rnge_start, rnge_end = rnge

        if rnge_start < overlap_start:
            result.add((rnge_start, overlap_start))

        if rnge_end > overlap_end:
            result.add((overlap_end, rnge_end))

        return result

    def process_seed_ranges(
        self, seeds: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        ranges = set(seeds)

        for mapping_type in self.almanac.keys():
            if mapping_type != "seeds":
                shifted_ranges: set[tuple[int, int]] = set()
                for to, start, length in self.almanac[  # pyright: ignore
                    mapping_type
                ]:
                    for rnge in ranges.copy():
                        if overlap := self._find_overlap(
                            rnge, (start, start + length)  # pyright: ignore
                        ):
                            ranges.remove(rnge)
                            ranges |= self._split_range(rnge, overlap)
                            shifted_ranges.add(
                                self._shift_range(
                                    overlap, to - start  # pyright: ignore
                                )
                            )

                ranges |= shifted_ranges

        return list(ranges)

    def find_mapping(
        self, src_num: int, mapping_type: str
    ) -> int:  # pyright: ignore
        for dest, src, rnge in self.almanac[mapping_type]:  # pyright: ignore
            if src <= src_num <= src + rnge:
                return dest + (src_num - src)  # pyright: ignore
        return src_num

    def find_location(self, seed: int) -> int:
        cur_value = seed
        for mapping_type in self.almanac.keys():
            if mapping_type != "seeds":
                cur_value = self.find_mapping(cur_value, mapping_type)

        return cur_value

    def find_min_location(self) -> int:
        location = float("inf")
        for seed_range in self.almanac["seeds"]:
            if not isinstance(seed_range, tuple):
                # Single seed
                location = min(self.find_location(seed_range), location)

        return location  # pyright: ignore

    def _process_seed(self, seed_val: int) -> int:
        return int(self.find_location(seed_val))


class TestMain(TestCase):
    def test_part1(self):
        test = Day05(f"{Path(__file__).parent}/test_input_part1.txt")
        self.assertEqual(test.find_mapping(53, "seed-to-soil"), 55)
        self.assertEqual(test.find_min_location(), 35)

    def test_part2(self):
        test = Day05(
            f"{Path(__file__).parent}/test_input_part2.txt", part_two=True
        )
        self.assertEqual(
            min(
                min(
                    test.process_seed_ranges(
                        test.almanac["seeds"]  # pyright: ignore
                    )
                )
            ),
            46,
        )


if __name__ == "__main__":
    # Part 1
    solution = Day05(f"{Path(__file__).parent}/input.txt")
    print(solution.find_min_location())
    # Part 2
    solution = Day05(f"{Path(__file__).parent}/input.txt", part_two=True)
    print(
        min(
            min(
                solution.process_seed_ranges(
                    solution.almanac["seeds"]  # pyright: ignore
                )
            )
        )
    )
