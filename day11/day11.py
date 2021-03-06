import os
import itertools


def count_seats(seat_map, row, col, visible=False):
    # Seats to check around
    directions = filter(lambda x: not x[0] == x[1] == 0,
                        itertools.product([-1, 0, 1], [-1, 0, 1]))

    count = 0
    for direction in directions:
        # Check adjacent seats
        if not visible:
            adj_seat = (col + direction[0], row + direction[1])
            if 0 <= adj_seat[0] <= len(
                    seat_map[0]) - 1 and 0 <= adj_seat[1] <= len(seat_map) - 1:
                count += 1 if seat_map[adj_seat[1]][adj_seat[0]] == "#" else 0

        # Check visible seats
        else:
            mult = 1
            occupied = False
            # Search until end of map or occupied seat found
            while not occupied:
                adj_seat = (
                    col + direction[0] * mult,
                    row + direction[1] * mult)
                if 0 <= adj_seat[0] <= len(
                        seat_map[0]) - 1 and 0 <= adj_seat[1] <= len(seat_map) - 1:
                    if seat_map[adj_seat[1]][adj_seat[0]] == ".":
                        mult += 1
                    else:
                        occupied = True
                        count += 1 if seat_map[adj_seat[1]
                                               ][adj_seat[0]] == "#" else 0
                else:
                    occupied = True

    return count


def count_occupied(seat_map):
    count = sum([row.count("#") for row in seat_map])

    return count


def seat_sim(seat_map, thresh, visible=False, change_state=True):
    while change_state:
        next_map = []
        for row in range(len(seat_map)):
            new_row = ""
            for col in range(len(seat_map[row])):
                # Count seat based on rule
                count = count_seats(seat_map, row, col, visible)

                # Replace seat layout
                if seat_map[row][col] == "L" and count == 0:
                    new_row += "#"
                elif seat_map[row][col] == "#" and count >= thresh:
                    new_row += "L"
                else:
                    new_row += seat_map[row][col]

            next_map.append(new_row)
        # Check state of seat layout
        if next_map == seat_map:
            change_state = False
        else:
            seat_map = next_map

    return seat_map


def main():
    # Read and create seat layout
    seat_file = input("Enter file containing seat layout: ")

    with open(os.path.realpath(seat_file), "r") as in_file:
        seat_map = [l.strip() for l in in_file]

    # Part 1
    stable_map = seat_sim(seat_map, 4)
    print(
        f"The number of occupied seats after stability: {count_occupied(stable_map)}")

    # Part 2
    stable_map = seat_sim(seat_map, 5, visible=True)
    print(
        f"The number of occupied seats after stability: {count_occupied(stable_map)}")


if __name__ == "__main__":
    main()
