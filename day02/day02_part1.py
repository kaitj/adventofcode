import collections
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

        # Count number of items each character appears in password
        counter = collections.Counter(line[-1])

        # Check to see if password is valid
        if (counter[line[-2]] >= int(line[0])
            ) and (counter[line[-2]] <= int(line[1])):
            VALID_PW += 1

print("Number of valid passwords: {}".format(VALID_PW))
