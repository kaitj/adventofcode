use std::{env, fs};

pub mod aoc_cli;
pub mod commands;
pub mod runner;

pub use day::*;

mod day;
mod readme_benchmarks;
mod run_multi;
mod timings;

pub const ANSI_ITALIC: &str = "\x1b[3m";
pub const ANSI_BOLD: &str = "\x1b[1m";
pub const ANSI_RESET: &str = "\x1b[0m";

/// Helper function to read text file to string
#[must_use]
pub fn read_file(day: Day) -> String {
    let filepath = env::current_dir()
        .expect("Failed to get current directory")
        .join("data")
        .join(format!("day{day}"))
        .join("input.txt");
    fs::read_to_string(&filepath)
        .unwrap_or_else(|_| panic!("Could not open input file: {}", filepath.display()))
}

/// Helper to read multi-part text
#[must_use]
pub fn read_file_part(day: Day, part: u8) -> String {
    let filepath = env::current_dir()
        .expect("Failed to get current directory")
        .join("data")
        .join(format!("day{day}"))
        .join(format!("input-{part}.txt"));
    fs::read_to_string(&filepath)
        .unwrap_or_else(|_| panic!("Could not open input file: {}", filepath.display()))
}

#[must_use]
pub fn read_example(day: Day) -> String {
    let filepath = env::current_dir()
        .expect("Failed to get current directory")
        .join("data")
        .join(format!("day{day}"))
        .join("example.txt");
    fs::read_to_string(&filepath)
        .unwrap_or_else(|_| panic!("Could not open example file: {}", filepath.display()))
}

/// Macro to setup input and runner for each part
#[macro_export]
macro_rules! solution {
    ($day:expr) => {
        $crate::solution!(@impl $day, [part_one, 1], [part_two, 2]);
    };
    ($day:expr, 1) => {
        $crate::solution!(@impl $day, [part_one, 1]);
    };
    ($day:expr, 2) => {
        $crate::solution!(@impl $day, [part_two, 2]);
    };

    (@impl $day:expr, $( [$func:expr, $part: expr] )*) => {
        const DAY: $crate::$template::Day = $crate::day!($day);

        #[cfg(feature = "dhat-heap")]
        #[global_allocator]
        static ALLOC: dhat::Alloc = dhat::Alloc;

        fn main() {
            use $crate::template::runner::*;
            let input = $crate::template::read_file(DAY);
            $( run_part($func, &input, DAY, &part); )*
        }
    };
}
