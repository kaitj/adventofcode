//! Wrapper module around `aoc-cli`
use std::{
    env,
    fmt::Display,
    process::{Command, Output, Stdio},
};

use crate::template::Day;

#[derive(Debug)]
pub enum AocCommandError {
    CommandNotFound,
    CommandNotCallable,
    BadExitStatus(Output),
}

impl Display for AocCommandError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AocCommandError::CommandNotFound => write!(f, "`aoc-cli` is not present."),
            AocCommandError::CommandNotCallable => write!(f, "`aoc-cli` could not be called."),
            AocCommandError::BadExitStatus(_) => {
                write!(f, "`aoc-cli` exited with non-zero status.")
            }
        }
    }
}

/// Check for availability of `aoc-cli`
pub fn check() -> Result<(), AocCommandError> {
    Command::new("aoc")
        .arg("-V")
        .output()
        .map_err(|_| AocCommandError::CommandNotFound)?;
    Ok(())
}

/// Read puzzle description for given day
pub fn read(day: Day) -> Result<Output, AocCommandError> {
    let puzzle_path = &get_puzzle_path(day);

    let args = build_args(
        "read",
        &[
            "--description-only",
            "--puzzle-file",
            puzzle_path,
        ],
        day,
    );

    call_aoc_cli(&args)
}

// Download input and puzzle description
pub fn download(day: Day) -> Result<Output, AocCommandError> {
    let args = build_args(
        "download",
        &[
            "--overwrite",
            "--input-file",
            &get_input_path(day),
            "--puzzle-file",
            &get_puzzle_path(day),
        ],
        day,
    );

    let output = call_aoc_cli(&args)?;
    println!(
        "🎄 Successfully wrote input to \"{}\" and puzzle to \"{}\".",
        get_input_path(day),
        get_puzzle_path(day),
    );
    Ok(output)
}

pub fn submit(day: Day, part: u8, result: &str) -> Result<Output, AocCommandError> {
    let mut args = build_args("submit", &[], day);
    args.push(part.to_string());
    args.push(result.to_string());
    call_aoc_cli(&args)
}

/// Generate input file path for given day
fn get_input_path(day: Day) -> String {
    format!("data/day{day}/input.txt")
}

/// Generate puzzle file path for given day
fn get_puzzle_path(day: Day) -> String {
    format!("data/day{day}/puzzle.md")
}

/// Fetch current year from env variable if set
fn get_year() -> Option<u16> {
    env::var("AOC_YEAR").ok()?.parse().ok()
}

/// Build arg list
fn build_args(command: &str, args: &[&str], day: Day) -> Vec<String> {
    let mut cmd_args: Vec<String> = args.iter().map(|&s| s.into()).collect();

    if let Some(year) = get_year() {
        cmd_args.push("--year".to_string());
        cmd_args.push(year.to_string());
    }

    cmd_args.push("--day".to_string());
    cmd_args.push(day.to_string());
    cmd_args.push(command.to_string());

    cmd_args
}

/// Call command with provided args
fn call_aoc_cli(args: &[String]) -> Result<Output, AocCommandError> {
    let output = Command::new("aoc")
        .args(args)
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .output()
        .map_err(|_| AocCommandError::CommandNotCallable)?;

    if output.status.success() {
        Ok(output)
    } else {
        Err(AocCommandError::BadExitStatus(output))
    }
}
