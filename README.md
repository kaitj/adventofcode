# Advent of Code 2023

My solutions to the exercises at https://adventofcode.com/2023, completed in
Python.

## Notes

## Setup

First grab your session cookie from your browser and save it to a `.cookie` file in the
top-level directory. This will allow you to grab your associated input directly, as well
as submit your solution via the terminal. Afterwards, setup your AoC virtual environment
by running the following:

```bash
poetry install
```

The code base for a given day can be initialized (which will also grab your specific
input) by running:

```bash

poetry run init_day <day>
```

If you want to test your code against the test cases (you will have to
copy and paste the examples into the `test_*.txt` file):

```bash
poetry run submit <day> -p <part> -t
```

To run the code for any particular day without submitting your solution:

```bash
poetry run submit <day> -p <part> -n
```

If you also wish to automatically submit your solution (assuming you have saved the
session cookie), you can run:

```bash
poetry run submit <day> -p <part>
```

_Note: For each of the previous 3 commands, `part` is a choice between `1` or `2` to
indicate the part of the puzzle being tested / run._

## Progress

<!-- ✓ -->

| Day | Name                                                                      | Progress |
| :-: | :------------------------------------------------------------------------ | :------: |
| 01  | [The Tyranny of the Rocket Equation](https://adventofcode.com/2019/day/1) |    ✓     |
| 02  | [1202 Program Alarm](https://adventofcode.com/2019/day/2)                 |    ✓     |
| 03  | [Crossed Wires](https://adventofcode.com/2019/day/3)                      |    ✓     |
