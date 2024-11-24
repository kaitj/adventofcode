use std::process;

use crate::template::{aoc_cli, Day};

pub fn handle(day: Day) {
    if aoc_cli::check().is_err() {
        eprintln!("Command \'aoc\' not found or not collable.");
        process::exit(1);
    }

    if let Err(e) = aoc_cli::download(day) {
        eprintln! {"Failed to call aoc-cli: {e}"};
        process::exit(1);
    }
}
