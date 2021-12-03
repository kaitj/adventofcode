import utils


def count_bits(in_data):
    bit_counter = {
        "0": dict.fromkeys(range(len(in_data[0])), 0),
        "1": dict.fromkeys(range(len(in_data[0])), 0),
    }

    for row_data in in_data:
        for idx, col in enumerate(row_data):
            bit_counter[col][idx] += 1

    return bit_counter


def compare_value(bit_counter, idx, gt=True):
    if gt:
        return "0" if bit_counter["0"][idx] > bit_counter["1"][idx] else "1"
    else:
        return "0" if bit_counter["0"][idx] <= bit_counter["1"][idx] else "1"


def compute_gamma(bit_counter):
    return "".join(
        compare_value(bit_counter, idx) for idx in range(len(bit_counter["0"].keys()))
    )


def compute_epsilon(bit_counter):
    return "".join(
        compare_value(bit_counter, idx, False)
        for idx in range(len(bit_counter["0"].keys()))
    )


def compute_o2(in_data):
    final_code = in_data.copy()

    for idx in range(len(in_data[0])):
        bit_count = count_bits(final_code)

        keep_bit = (
            "1"
            if bit_count["0"][idx] == bit_count["1"][idx]
            else compare_value(bit_count, idx)
        )

        final_code = [val for val in final_code if val[idx] == keep_bit]

        if len(final_code) == 1:
            break

    return final_code[0]


def compute_co2(in_data):
    final_code = in_data.copy()

    for idx in range(len(in_data[0])):
        bit_count = count_bits(final_code)

        keep_bit = (
            "0"
            if bit_count["0"][idx] == bit_count["1"][idx]
            else compare_value(bit_count, idx, gt=False)
        )

        final_code = [val for val in final_code if val[idx] == keep_bit]

        if len(final_code) == 1:
            break

    return final_code[0]


def puzzle1(in_data):
    bit_counts = count_bits(in_data)

    gamma = compute_gamma(bit_counts)
    epsilon = compute_epsilon(bit_counts)

    return int(gamma, 2) * int(epsilon, 2)


def puzzle2(in_data):
    o2 = compute_o2(in_data)
    co2 = compute_co2(in_data)

    return int(o2, 2) * int(co2, 2)


if __name__ == "__main__":
    in_data = input("Enter file path of diagnostic report: ")
    in_fpath = utils.parse_group(in_data)

    # Puzzle 1
    print(f"The power consumption is: {puzzle1(in_fpath)}")

    # Puzzle 2
    print(f"The life support rating is: {puzzle2(in_fpath)}")
