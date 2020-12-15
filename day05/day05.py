import os


def search_seatid(boarding_pass):
    # Binarize ID
    id_letter = "FBLR"
    id_num = "0101"
    id_trans = str.maketrans(id_letter, id_num)

    binary_id = boarding_pass.translate(id_trans)
    seat_id = int(binary_id[:7], 2) * 8 + int(binary_id[-3:], 2)

    return seat_id


def search_open_seat(seat_ids):
    possible_seats = set(range(min(seat_ids), max(seat_ids)))
    open_seats = list(set(seat_ids) ^ possible_seats)

    for seat in open_seats:
        if (seat - 1 in seat_ids) and (seat + 1 in seat_ids):
            open_seat = seat

    return open_seat


def main():
    # User input
    boarding_file = input("Enter the file containing the boarding passes: ")

    # Open file and search for seat
    with open(os.path.realpath(boarding_file), "r") as in_file:
        seat_ids = [search_seatid(boarding_pass.strip("\n"))
                    for boarding_pass in in_file]

    print("Highest seat ID on a boarding pass: {}".format(max(seat_ids)))

    # Search for open seat
    open_seat = search_open_seat(seat_ids)
    print("Open seat at: {}".format(open_seat))


if __name__ == "__main__":
    main()
