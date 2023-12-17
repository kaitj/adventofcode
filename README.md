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

| Day | Name                                                                   | Progress |
| :-: | :--------------------------------------------------------------------- | :------: |
| 01  | [Trebuchet?](https://adventofcode.com/2023/day/1)                      |    ✓     |
| 02  | [Cube Conundrum](https://adventofcode.com/2023/day/2)                  |    ✓     |
| 03  | [Gear Ratios](https://adventofcode.com/2023/day/3)                     |    ✓     |
| 04  | [Scratchcards](https://adventofcode.com/2023/day/4)                    |    ✓     |
| 05  | [If You Give A Seed A Fertilizer](https://adventofcode.com/2023/day/5) |    ✓     |
| 06  | [Wait For It](https://adventofcode.com/2023/day/6)                     |    ✓     |
| 07  | [Camel Cards](https://adventofcode.com/2023/day/7)                     |    ✓     |
| 08  | [Haunted Wasteland](https://adventofcode.com/2023/day/8)               |    ✓     |
| 09  | [Mirage Maintenance](https://adventofcode.com/2023/day/9)              |    ✓     |
| 10  | [Pipe Maze](https://adventofcode.com/2023/day/10)                      |    ✓     |
| 11  | [Cosmic Expansion](https://adventofcode.com/2023/day/11)               |    ✓     |
| 12  | [Hot Springs](https://adventofcode.com/2023/day/12)                    |    ✓     |
| 13  | [Point of Incidence](https://adventofcode.com/2023/day/13)             |    ✓     |
| 14  | [Parabolic Reflector Dish](https://adventofcode.com/2023/day/14)       |    ✓     |
| 15  | [Lens Library](https://adventofcode.com/2023/day/15)                   |    ✓     |
| 16  | [The Floor Will Be Lava](https://adventofcode.com/2023/day/16)         |    ✓     |
| 17  | [Clumsy Crucible](https://adventofcode.com/2023/day/17)                |    ✓     |
