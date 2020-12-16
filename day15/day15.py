import os
from collections import defaultdict, deque


def spoken_num(spoken_numbers, iteration):
    mem = defaultdict(deque)

    # Check number of times previous number has been spoken
    for i in range(iteration):
        if i < len(spoken_numbers):
            mem[spoken_numbers[i]].append(i)
        elif len(mem[spoken_numbers[-1]]) == 1:
            if len(mem[0]) > 2:
                mem[0].popleft()
            mem[0].append(i)
            spoken_numbers.append(0)
        else:
            diff = mem[spoken_numbers[-1]][-1] - mem[spoken_numbers[-1]][-2]
            if len(mem[diff]) > 2:
                mem[diff].popleft()
            mem[diff].append(i)
            spoken_numbers.append(diff)

    return spoken_numbers[-1]


def main():
    numbers_file = input("Enter the file containing the numbers spoken: ")

    with open(os.path.realpath(numbers_file), "r") as in_file:
        starting_numbers = in_file.read().split(',')
    starting_numbers = [int(num) for num in starting_numbers]

    # Part 1
    print(f"The 2020th number spoken is: {spoken_num(starting_numbers, 2020)}")

    # Part 2
    print(f"The 300000000th number spoken is: \
            {spoken_num(starting_numbers, 30000000)}")


if __name__ == "__main__":
    main()
