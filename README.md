# Advent of Code 2024

Solutions for [2024](https://adventofcode.com/2024), completed in
[Rust](https://www.rust-lang.org/).

## Setup

> [!IMPORTANT]
> This repository makes use of [aoc-cli](https://github.com/scarvalhojr/aoc-cli) to read
> and submit puzzle solutions. To install the crate, call the following:
> `cargo install aoc-cli` to install the latest version.

To automatically download the input, as well as upload solutions, you will need to
retrieve your session cookie. To do so, use the dev tools in your browser, and copy the
`session` cookie value under _Application_ or _Storage_.

> [!IMPORTANT]
> See the different ways that the session cookie can be stored
> [here](https://github.com/scarvalhojr/aoc-cli/tree/main?tab=readme-ov-file#session-cookie-).
> If you are uploading your solutions to a public repository, it is recommended to store
> the session locally.

## Usage

> [!NOTE]
> Aliases are created to be able to call `cargo <command>` in this package. Check out
> the configuration file [here](./.cargo/config.toml).

### Scaffold

```sh
# example: `cargo scaffold 1`
cargo scaffold <day>

# output:
# Created module file "src/bin/01.rs"
# Created empty input file "data/inputs/01.txt"
# Created empty example file "data/examples/01.txt"
# ---
# 🎄 Type `cargo solve 01` to run your solution.
```

Solutions live in `src/bin/` as separate binaries.
_Inputs_ and _examples_ can be found in the `data/` directory.

Each solution has _tests_ referencing its _example_ file in `data/examples`. Use these
tests to develop and debug solutions against the example input.

> [!TIP]
> If a day has multiple example inputs, `read_file_part()` can be used in tests in place
> of `read_file()`. To create an example file for the second part, e.g. for day 1,
> name the file like `day01-2.txt` and invoke the helper like
> `let result = part_two(&adventofcode::template::read_file_part("examples", DAY, @));`.
> This supports an arbitrary number of example files.

### Download input

Puzzle inputs and descriptions can be downloaded by either appending the `--download`
flag to the `scaffold` command or with by separately calling `download`:

```sh
# example: `cargo download 1`
cargo download <day>

# output
# [INFO  aoc] 🎄 aoc-cli - Advent of Code command-line tool
# [INFO  aoc_client] 🎅 Saved puzzle to 'data/puzzles/day01.md'
# [INFO  aoc_client] 🎅 Saved input to 'data/inputs/day01.txt'
# ---
# 🎄 Successfully wrote input to "data/inputs/day01.txt".
# 🎄 Successfully wrote puzzle to "data/puzzles/day01.md".
```

### Run individual solution

```sh
# example: `cargo solve 01`
cargo solve <day>

# output:
#     Finished dev [unoptimized + debuginfo] target(s) in 0.13s
#     Running `target/debug/01`
# Part 1: 42 (166.0ns)
# Part 2: 42 (41.0ns)
```

To run an optimized build, append the `--release` flag.

> [!TIP]
> Append `--submit <part>` option to the `solve`command to submit your solution.

### Run all solutions

```sh
cargo all

# output:
#     Running `target/release/advent_of_code`
# ----------
# | Day 01 |
# ----------
# Part 1: 42 (19.0ns)
# Part 2: 42 (19.0ns)
# <...other days...>
# Total: 0.20ms
```

### Benchmark solutions

```sh
cargo time <day> [--all] [--store]

# output:
# Day 08
# ------
# Part 1: 1 (39.0ns @ 10000 samples)
# Part 2: 2 (39.0ns @ 10000 samples)
#
# Total (Run): 0.00ms
#
# Stored updated benchmarks.
```

The `cargo time` command provides a method to benchmark code and store timings in the
README. When benchmarking, the runner will run the code between `10` and `10_000` times,
printing the average execution time.

There are three modes of execution:

1. `cargo time` without arguments incrementally benchmarks solutions that have not been
   stored in the README, skipping the rest
2. `cargo time <day>` benchmarks a single day's solution
3. `cargo time --all` benchmarks all solutions

By default, the command does not write to the README - to do so, append the `--store`
flag.

> [!NOTE]
> These benchmarks are an approximation and are by no means exhaustive.

### Testing

```sh
cargo test
```

To run tests for a specific day, append `--bin <day>`. This can be further scoped to a
specific part (e.g. `cargo test --bin <day> part_one`).

### Read puzzle

```sh
# example: `cargo read 1`
cargo read <day>

# output:
# Loaded session cookie from "/Users/<snip>/.adventofcode.session".
# Fetching puzzle for day 1, 2022...
# ...the input...
```

### Current day

During the days of advent of code, `cargo today` can be used to:

- scaffold the solution
- download the input
- read the puzzle

```sh
# example: `cargo today` on December 1st
cargo today

# output:
# Created module file "src/bin/01.rs"
# Created empty input file "data/inputs/01.txt"
# Created empty example file "data/examples/01.txt"
# ---
# 🎄 Type `cargo solve 01` to run your solution.
# [INFO  aoc] 🎄 aoc-cli - Advent of Code command-line tool
# [INFO  aoc_client] 🎅 Saved puzzle to 'data/puzzles/01.md'
# [INFO  aoc_client] 🎅 Saved input to 'data/inputs/01.txt'
# ---
# 🎄 Successfully wrote input to "data/inputs/01.txt".
# 🎄 Successfully wrote puzzle to "data/puzzles/01.md".
#
# Loaded session cookie from "/Users/<snip>/.adventofcode.session".
# Fetching puzzle for day 1, 2022...
# ...the input...
```

### Format

```sh
cargo fmt
```

### Lint

```sh
cargo clippy
```

## Progress

<!-- :star: -->

| Day | Name                                                      | Part 1 | Part 2 |
| :-: | :-------------------------------------------------------- | :----: | :----: |
| 01  | [Historian Hysteria](https://adventofcode.com/2024/day/1) | :star: | :star: |
