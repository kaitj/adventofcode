#!/bin/bash
# This is a small script to setup files for AOC day
# Ensure at least 2 digits (e.g. 01, 02, 10, 11, etc.)
day=$1
while [[ ${#day} -lt 2 ]]; do
  day="0${day}"
done

# Create folder
day_prefix=Day${day}
mkdir -p $day_prefix

# Create python file
py_file=${day_prefix}/${day_prefix}.py
echo "#!/usr/bin/env python" > ${py_file}
echo "from pathlib import Path" >> ${py_file}
echo "from unittest import TestCase" >> ${py_file}
echo "" >> ${py_file}
echo "class ${day_prefix}:" >> ${py_file}
echo "" >> ${py_file}
echo "class TestMain(TestCase):" >> ${py_file}
echo "    def test_part1(self):" >> ${py_file}
echo "        test = ${day_prefix}(f'{Path(__file__).parent}/test_input_part1.txt')" >> ${py_file}
echo "" >> ${py_file}
echo "    # def test_part2(self):" >> ${py_file}
echo "    #     test = ${day_prefix}(f'{Path(__file__).parent}/test_input_part2.txt')" >> ${py_file}
echo "" >> ${py_file}
echo "# if __name__ == '__main__':" >> ${py_file}
echo "#     solution = ${day_prefix}(f'{Path(__file__).parent}/input.txt')" >> ${py_file}

# Create input files
touch ${day_prefix}/input.txt
touch ${day_prefix}/test_input_part1.txt
touch ${day_prefix}/test_input_part2.txt
