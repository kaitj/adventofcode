import os
import math


def find_earliest(busses, timestamp):
    min_diff = min_bus = None

    for bus in busses:
        time_diff = math.ceil(timestamp / bus) * bus - timestamp

        if min_diff is None or time_diff < min_diff:
            min_bus = bus
            min_diff = time_diff

    return min_bus, min_diff


def least_common_multiple(num1, num2):
    lcm = int((num1 * num2) / math.gcd(num1, num2))

    return lcm


def no_limit_departure(busses):
    # Get busses and offsets
    info = [(time, int(bus)) for time, bus in enumerate(busses) if bus != "x"]
    to_check = len(info)

    # Initialize timestamp and step size
    timestamp, t_step = 0, info[0][1]

    # Loop through remaining busses
    # Find step size and increment time stamp until correct bus timestamp found
    while to_check:
        t_offset, bus = info[len(info) - to_check]
        # Find new step size if bus leaves at correct time offset
        if (timestamp + t_offset) % bus == 0:
            t_step = least_common_multiple(t_step, bus)
            to_check -= 1
        else:
            timestamp += t_step

    return timestamp


def main():
    # Read and extract infos
    bus_file = input("Enter file containing timestamp and running busses: ")

    with open(os.path.realpath(bus_file), "r") as in_file:
        info = [info.strip() for info in in_file]

    # Sort timestamp and busses
    timestamp = int(info[0])

    # Part 1
    busses_1 = map(int, filter(lambda b: b != "x", info[1].split(',')))
    min_bus, min_diff = find_earliest(busses_1, timestamp)
    mult_bus = min_bus * min_diff
    print(
        f"The multiplication of the earliest bus and time difference is: {mult_bus}")

    # Part 2
    busses_2 = list(info[1].split(','))
    print("The earliest timestamp where subsequent "
          f"departures happen is at: {no_limit_departure(busses_2)}")


if __name__ == "__main__":
    main()
