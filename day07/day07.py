import utils


def calc_fuel(start_position: int, end_position: int, const: bool = False) -> int:
    const_burn = abs(start_position - end_position)
    return const_burn if not const else ((const_burn ** 2 + const_burn) // 2)


def find_min_fuel(start_positions: list[int], const: bool = False) -> int:
    return min(
        sum(
            calc_fuel(start_position, end_position, const)
            for start_position in start_positions
        )
        for end_position in range(max(start_positions))
    )


if __name__ == "__main__":
    in_fpath = input("Enter file containing starting positions: ")
    in_data = utils.parse_line(in_fpath, ",", int)

    print(f"Minimum fuel required (constant burn): {find_min_fuel(in_data)}")

    print(f"Minimum fuel required (non-constant burn): {find_min_fuel(in_data, True)}")
