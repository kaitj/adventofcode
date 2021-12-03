import utils


def compare_values(val1: int, val2: int):
    return val2 > val1


def count_larger(in_data):
    count = 0
    for idx in range(1, len(in_data)):
        if compare_values(in_data[idx - 1], in_data[idx]):
            count += 1

    return count


def compute_window(in_data, window=3):
    return [
        sum(in_data[idx : idx + window]) for idx in range(len(in_data) - window + 1)
    ]


if __name__ == "__main__":
    data_fpath = input("Enter the path to the file: ")
    data_content = utils.parse_lines(data_fpath, int)

    # Puzzle 1
    print(f"Number of larger elements in list: {count_larger(data_content)}")

    # Puzzle 2
    windowed_data = compute_window(data_content)
    print(f"Number of larger elements in window: {count_larger(windowed_data)}")
