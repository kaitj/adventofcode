import os
import re

# User input
input_pw = input("Enter the path to the input file: ")

# Sort into dictionary
pw_dict = {}
VALID_PW = 0

with open(os.path.realpath(input_pw), "r") as f:
    for line in f:
        # Remove non alphanumeric and split
        line = re.sub(r"[^\w]", ' ', line)
        line = line.split()

        # Check to see if password is valid
        if (line[-1][int(line[0]) - 1] == line[-2]
            ) ^ (line[-1][int(line[1]) - 1] == line[-2]):
            VALID_PW += 1

print("Number of valid passwords: {}".format(VALID_PW))
