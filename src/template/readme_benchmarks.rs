//! Module updating readme with timing information
use std::{fs, io, ops::Range};

use crate::template::timings::Timings;
use crate::template::Day;

static MARKER: &str = "<!--- benchmarking table -->";

#[allow(dead_code)]
#[derive(Debug)]
pub enum Error {
    Parser(String),
    IO(io::Error),
}

impl From<std::io::Error> for Error {
    fn from(e: std::io::Error) -> Self {
        Error::IO(e)
    }
}

#[must_use]
pub fn get_path_for_bin(day: Day) -> String {
    format! {"./src/bin/{day}.rs"}
}

fn locate_table(readme: &str) -> Result<Range<usize>, Error> {
    let matches: Vec<_> = readme.match_indices(MARKER).collect();

    match matches.as_slice() {
        [start, end] => Ok(start.0..end.0 + end.1.len()),
        [] => Err(Error::Parser(
            "Could not find marker in README.".to_string(),
        )),
        _ => Err(Error::Parser("Too many markers in README.".to_string())),
    }
}

fn construct_table(prefix: &str, timings: &Timings, total_millis: f64) -> String {
    let mut lines = vec![
        MARKER.to_string(),
        format!("{prefix} Benchmarks"),
        String::new(),
        "| Day | Part 1 | Part 2 |".to_string(),
        "| :---: | :---: | :---: |".to_string(),
    ];

    lines.extend(timings.data.iter().map(|timing| {
        let path = get_path_for_bin(timing.day);
        format!(
            "| [Day {}]({}) | `{}` | `{}` |",
            timing.day.into_inner(),
            path,
            timing.part_1.as_deref().unwrap_or("-"),
            timing.part_2.as_deref().unwrap_or("-"),
        )
    }));

    lines.push(String::new());
    lines.push(format!("**Total: {total_millis:.2}ms**"));
    lines.push(MARKER.to_string());

    lines.join("\n")
}

fn update_content(readme: &mut String, timings: &Timings, total_millis: f64) -> Result<(), Error> {
    let range = locate_table(readme)?;
    let table = construct_table("##", timings, total_millis);
    readme.replace_range(range, &table);
    Ok(())
}

pub fn update(timings: Timings) -> Result<(), Error> {
    let path = "README.md";
    let mut readme = fs::read_to_string(path)?;
    let total_millis = timings.total_millis();
    update_content(&mut readme, &timings, total_millis)?;
    fs::write(path, readme)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::day;
    use crate::template::timings::{Timing, Timings};

    fn mock_timings() -> Timings {
        Timings {
            data: vec![Timing {
                day: day!(1),
                part_1: Some("10ms".to_string()),
                part_2: Some("20ms".to_string()),
                total_nanos: 3e+10,
            }],
        }
    }

    #[test]
    fn errors_if_marker_not_present() {
        let mut content = "No marker here".to_string();
        assert!(update_content(&mut content, &mock_timings(), 190.0).is_err());
    }

    #[test]
    fn errors_if_multiple_markers_present() {
        let mut content = format!("{MARKER} {MARKER} {MARKER}");
        assert!(update_content(&mut content, &mock_timings(), 190.0).is_err());
    }

    #[test]
    fn updates_empty_benchmarks() {
        let mut content = format!("{MARKER} {MARKER}");
        update_content(&mut content, &mock_timings(), 190.0).unwrap();
        assert!(content.contains("## Benchmarks"));
    }

    #[test]
    fn updates_existing_benchmarks() {
        let mut content = format!("foo\nbar\n{MARKER}{MARKER}\nbaz");
        update_content(&mut content, &mock_timings(), 190.0).unwrap();
        assert!(content.contains("## Benchmarks"));
    }

    #[test]
    fn formats_correctly() {
        let mut content = format!("{MARKER}{MARKER}");
        update_content(&mut content, &mock_timings(), 190.0).unwrap();

        let expected = vec![
            MARKER,
            "## Benchmarks",
            "",
            "| Day | Part 1 | Part 2 |",
            "| :---: | :---: | :---: |",
            "| [Day 1](./src/bin/day01.rs) | `10ms` | `20ms` |",
            "",
            "**Total: 190.00ms**",
            MARKER,
        ]
        .join("\n");

        assert_eq!(content, expected);
    }
}
