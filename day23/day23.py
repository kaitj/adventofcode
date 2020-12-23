import os


def setup_game(cups_input, part1=True):
    cups = {}

    i_idx = 0
    for j_idx in range(1, len(cups_input)):
        cups[cups_input[i_idx]] = cups_input[j_idx]
        i_idx += 1

    if part1:
        # Wrap end back to beginning
        cups[cups_input[i_idx]] = cups_input[0]
    else:
        # Add other cups for part 2
        cups[cups_input[len(cups_input) - 1]] = max(cups_input) + 1
        for i_idx in range(max(cups_input) + 1, 1000000):
            cups[i_idx] = i_idx + 1
        cups[1000000] = cups_input[0]

    return cups


def play_round(cups, current):
    # Pick up 3 cups
    one = cups[current]
    two = cups[one]
    three = cups[two]

    pickup = (one, two, three)

    # Find destination and wrap if needed
    destination = current - 1

    if destination < 1:
        destination = max(cups.keys())

    while destination in pickup:
        destination -= 1
        if destination < 1:
            destination = max(cups.keys())

    # Rearrange pointers after round
    cups[current] = cups[three]
    cups[three] = cups[destination]
    cups[destination] = one


def get_order(cups, start):
    cup_order = ""

    current = start
    while len(cup_order) < len(cups):
        cup_order += str(cups[current])
        current = cups[current]

    return cup_order[:-1]


def play_game(cups_input, rounds, part1=True):
    cups = setup_game(cups_input, part1=part1)

    current = int(cups_input[0])
    rnd = 1

    for _ in range(rounds):
        if rnd % 2500000 == 0:
            print(f"Round: {rnd}")
        # Update current position
        if rnd != 1:
            current = cups[current]
        # Play a round
        play_round(cups, current)
        rnd += 1

    return get_order(cups, 1) if part1 else cups[1] * cups[cups[1]]


def main():
    cups_file = input("Enter file containing cups: ")

    with open(os.path.realpath(cups_file), "r") as in_file:
        cups_input = list(map(int, in_file.read()))

    # Part 1
    cup_order = play_game(cups_input, 100)
    print(f"Cup labels after 100 moves: {cup_order}")

    # Part 2
    cup_product = play_game(cups_input, 10000000, part1=False)
    print(f"Product of cups with stars is: {cup_product}")


if __name__ == '__main__':
    main()
