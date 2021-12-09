import utils


def count_unique(digit_list: list[str]) -> int:
    return sum(len(digit) in [2, 3, 4, 7] for digit in digit_list.split(" "))


def solve_segment(
    pattern: list[str],
    segments: int,
    found_pattern: str = None,
    matching_segments: int = None,
):
    # First possible patterns, then narrow down to those matching segments of already found digits
    subset = filter(lambda x: len(x) == segments, pattern)
    if found_pattern:
        subset = filter(lambda x: len(x & found_pattern) == matching_segments, subset)

    subset = list(subset)

    # Check there is only a single pattern found
    try:
        assert len(subset) == 1
    except:
        print(subset)
        raise AssertionError("More than 1 possible pattern found")

    pattern.remove(subset[0])

    return subset[0]


def decode_pattern(pattern):
    pattern = list(map(set, pattern))
    segment_map = [set()] * 10

    # 1, 4, 7, 8 are known
    segment_map[1] = solve_segment(pattern, 2)
    segment_map[4] = solve_segment(pattern, 4)
    segment_map[7] = solve_segment(pattern, 3)
    segment_map[8] = solve_segment(pattern, 7)
    # Resolve rest by pattern matching intersections
    segment_map[9] = solve_segment(pattern, 6, segment_map[4], 4)
    segment_map[0] = solve_segment(pattern, 6, segment_map[1], 2)
    segment_map[6] = solve_segment(pattern, 6, segment_map[1], 1)
    segment_map[3] = solve_segment(pattern, 5, segment_map[1], 2)
    segment_map[2] = solve_segment(pattern, 5, segment_map[4], 2)
    segment_map[5] = pattern[0]

    reverse_segmap = list(map(frozenset, segment_map))

    return {
        decoded_pattern: value for value, decoded_pattern in enumerate(reverse_segmap)
    }


def puzzle1(in_data: str) -> int:
    return sum(count_unique(line.strip("\n").split(" | ")[-1]) for line in in_data)


def puzzle2(in_data: str) -> int:
    total = 0
    for line in in_data:
        pattern, digits = map(str.split, line.split(" | "))
        decoded_pattern = decode_pattern(pattern)
        total += int(
            "".join(map(str, [decoded_pattern[frozenset(digit)] for digit in digits]))
        )

    return total


if __name__ == "__main__":
    in_fpath = input("Enter the file path containing signal output: ")
    in_data = utils.parse_lines(in_fpath, str)

    # Puzzle 1
    print(f"Number of times unique digits appear: {puzzle1(in_data)}")

    # Puzzle 2
    print(f"Number of times unique digits appear: {puzzle2(in_data)}")
