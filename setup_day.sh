#!/bin/bash
# This is a small script to setup files for AOC day

# Ensure at least 2 digits (e.g. 01, 02, 10, 11, etc.)
day=$(printf "%02d" $1)
year=2023

# Create folder
day_prefix=Day${day}
mkdir -p "${day_prefix,,}"

# Checkout branch
git checkout -b "${year}/${day_prefix,,}"

# Create python file
py_file="${day_prefix,,}/${day_prefix,,}.py"
cat > $py_file << EOF
#!/usr/bin/env python
from pathlib import Path
from unittest import TestCase

class ${day_prefix}:

class TestMain(TestCase):
    def test_part1(self):
        test = ${day_prefix}(f"{Path(__file__).parent}/test_input_part1.txt")

    # def test_part2(self):
    #   test = ${day_prefix}(f"{Path(__file__).parent}/test_input_part2.txt")

# if __name__ == "__main__":
#   solution = ${day_prefix}(f"{Path(__file__).parent}/input.txt")
EOF

# Create input files
touch "${day_prefix,,}/input.txt"
touch "${day_prefix,,}/test_input_part1.txt"
touch "${day_prefix,,}/test_input_part2.txt"
