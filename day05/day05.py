#!/usr/bin/env python
import multiprocessing
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
                # Minimize overlapping
                combined_ranges = sorted(
                    (start, start + length)
                    for start, length in zip(
                        seed_ranges[::2], seed_ranges[1::2]
                    )
                )

                merged_ranges: list[tuple[int, int]] = []
                current_start, current_end = combined_ranges[0]
                for start, end in combined_ranges[1:]:
                    if start <= current_end:
                        current_end = max(current_end, end)
                    else:
                        merged_ranges.append((current_start, current_end))
                        current_start, current_end = start, end
                merged_ranges.append((current_start, current_end))

                almanac["seeds"] = merged_ranges  # pyright: ignore
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
        for seed in self.almanac["seeds"]:
            if not isinstance(seed, tuple):
                location = min(self.find_location(seed), location)
            else:
                print(seed)  # Processing check print statement
                with multiprocessing.Pool(processes=8) as pool_obj:
                    results = pool_obj.map(
                        self._process_seed, range(seed[0], seed[1])
                    )
                    location = min(results + [location])

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
        self.assertEqual(test.find_min_location(), 46)


if __name__ == "__main__":
    # Part 1
    solution = Day05(f"{Path(__file__).parent}/input.txt")
    print(solution.find_min_location())
    # Part 2
    solution = Day05(f"{Path(__file__).parent}/input.txt", part_two=True)
    print(solution.find_min_location())
