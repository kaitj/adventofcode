use std::{
    cmp, env,
    fmt::Display,
    hint::black_box,
    io::{stdout, Write},
    process::{self},
    time::{Duration, Instant},
};

use crate::template::{aoc_cli, Day, ANSI_BOLD, ANSI_ITALIC, ANSI_RESET};

/// Run solution for given part, handling timing, output, and optional sumbission
pub fn run_part<I: Clone, T: Display>(func: impl Fn(I) -> Option<T>, input: I, day: Day, part: u8) {
    let part_str = format!("Part {part}");

    let (result, duration, samples) =
        run_timed(func, input, |res| print_result(res, &part_str, ""));

    print_result(&result, &part_str, &format_duration(&duration, samples));

    if let Some(result) = result {
        submit_result(result, day, part);
    }
}

/// Execute function and measure execution time
/// Run one if in debug mode, or benchmark in release if `--time` is called
fn run_timed<I: Clone, T>(
    func: impl Fn(I) -> T,
    input: I,
    hook: impl Fn(&T),
) -> (T, Duration, u128) {
    let timer = Instant::now();
    let result = func(input.clone());
    let elapsed = timer.elapsed();

    hook(&result);

    let (duration, samples) = if env::args().any(|arg| arg == "--time") {
        bench(func, input, elapsed)
    } else {
        (elapsed, 1)
    };

    (result, duration, samples)
}

/// Benchmark function, running multiple times and averaging exec time
fn bench<I: Clone, T>(func: impl Fn(I) -> T, input: I, base_time: Duration) -> (Duration, u128) {
    print!(" > {ANSI_ITALIC}benching{ANSI_RESET}");
    stdout().flush().ok();

    let iterations =
        (Duration::from_secs(1).as_nanos() / cmp::max(base_time.as_nanos(), 10)).clamp(10, 10_000);

    let mut durations = Vec::with_capacity(iterations as usize);
    for _ in 0..iterations {
        let start = Instant::now();
        black_box(func(input.clone()));
        durations.push(start.elapsed());
    }

    let avg_duration = average_duration(&durations);
    (Duration::from_nanos(avg_duration as u64), iterations)
}

/// Compute average duration
fn average_duration(durations: &[Duration]) -> u128 {
    durations.iter().map(Duration::as_nanos).sum::<u128>() / durations.len() as u128
}

/// Format duration for display
fn format_duration(duration: &Duration, samples: u128) -> String {
    if samples == 1 {
        format!(" ({duration:.1?})")
    } else {
        format!(" ({duration:.1?} @ {samples} samples)")
    }
}

/// Print result of solution part, formatting based on result type
fn print_result<T: Display>(result: &Option<T>, part_label: &str, duration_str: &str) {
    match result {
        Some(value) => {
            let value_str = value.to_string();
            let formatted_result = if value_str.contains('\n') {
                format!("{part_label}: ▼ {duration_str}\n{value}")
            } else {
                format!("{part_label}: {ANSI_BOLD}{value}{ANSI_RESET}{duration_str}")
            };
            println!("\r{formatted_result}");
        }
        None => {
            let error_message = format!("{part_label}: ✖");
            println!("\r{error_message}");
        }
    }
}

/// Submit solution via `aoc-cli`
fn submit_result<T: Display>(result: T, day: Day, part: u8) {
    if !env::args().any(|arg| arg == "--submit") {
        return;
    }

    if let Some(submit_part) = parse_submit_part() {
        if submit_part != part {
            return;
        }
    }

    if aoc_cli::check().is_err() {
        eprintln!("Command `aoc` not found.");
        process::exit(1);
    }

    println!("Submitting result...");
    if let Err(err) = aoc_cli::submit(day, part, &result.to_string()) {
        eprintln!("Submission failed: {err}");
    }
}

/// Parse part number to submit
fn parse_submit_part() -> Option<u8> {
    let args: Vec<String> = env::args().collect();
    args.iter()
        .position(|arg| arg == "--submit")
        .and_then(|pos| args.get(pos + 1))
        .and_then(|part| part.parse().ok())
}
