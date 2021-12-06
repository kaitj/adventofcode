from collections import defaultdict

import utils


def count_fish(init_dates: list[int], num_days: int) -> int:
    # Count the number of fish per day
    fish_count = defaultdict(int)
    for dates in init_dates:
        fish_count[dates] += 1

    # Determine number of fish created after num_days
    for _ in range(num_days):
        new_fish_count = defaultdict(int)
        for days_left, fish_count in fish_count.items():
            if days_left == 0:
                # Reset timer and add same number of new fish
                new_fish_count[6] += fish_count
                new_fish_count[8] += fish_count
            else:
                # Minus 1 day for fish not due
                new_fish_count[days_left - 1] += fish_count

        # Update tracker
        fish_count = new_fish_count

    return sum(fish_count.values())


if __name__ == "__main__":
    input_data = input("Enter path containing fish due dates: ")
    fish_dates = utils.parse_line(input_data, ",", int)

    print(f"Number of laternfish after 80 days: {count_fish(fish_dates, 80)}")

    print(f"Number of laternfish after 256 days: {count_fish(fish_dates, 256)}")
