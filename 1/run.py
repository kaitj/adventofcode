import numpy as np
import itertools
import os

# User inputs for target sum, path to input, and number of entries
target_sum = int(input("Enter target sum: "))
input_list = input("Enter path to input list: ")
input_list = np.genfromtxt(os.path.realpath(input_list), dtype=int)
num_combinations = int(input("Enter number of entries: "))

# Find entries to target sum and return multiplication
for num in itertools.combinations(input_list, num_combinations):
    if sum(num) == target_sum:
        print("\nCombination of numbers: {0}".format(num))
        print("Multiplication result: {0}".format(np.product(num)))