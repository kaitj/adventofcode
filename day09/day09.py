import os 
import itertools

def find_missing(xmas_code, preamble):
    for l in range(0, len(xmas_code)):
        possible_sums = set([sum(combo) for combo in itertools.combinations(xmas_code[l:l+preamble], 2)])
        
        if not xmas_code[preamble+l] in possible_sums:
            return xmas_code[l+preamble]
        
    return None

def find_weakness(xmas_code, missing_num):
    for l in range(0, len(xmas_code)):
        combo_sum = [combo for combo in itertools.accumulate(xmas_code[l:])][1:]

        if missing_num in combo_sum:
            index = combo_sum.index(missing_num)
            combo = xmas_code[l:][:index+2]

            return min(combo) + max(combo)

    return None


def main():
    # User input
    xmas_file = input("Enter file containing XMAS-encrypted list: ")

    # Open file containing xmas code
    with open(os.path.realpath(xmas_file), "r") as f:
        xmas_code = f.read().split()
    xmas_code = list(map(int, xmas_code))

    # Part 1
    missing_num = find_missing(xmas_code, 25)
    print(f"First invalid number in XMAS-list is: {missing_num}")

    # Part 2
    weakness_sum = find_weakness(xmas_code, missing_num)
    print(f"The weakness in XMAS-list is: {weakness_sum}")

if __name__ == "__main__":
    main()