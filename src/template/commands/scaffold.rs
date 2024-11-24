use std::{
    fs::{File, OpenOptions},
    io::Write,
    process,
};

use crate::template::Day;

const MODULE_TEMPLATE: &str =
    include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/src/template.txt"));

fn safe_create_file(path: &str, overwrite: bool) -> Result<File, std::io::Error> {
    OpenOptions::new()
        .write(true)
        .truncate(true)
        .create(overwrite)
        .create_new(!overwrite)
        .open(path)
}

pub fn handle(day: Day, overwrite: bool) {
    let binding = MODULE_TEMPLATE.replace("%DAY_NUMBER%", &day.into_inner().to_string());
    let paths = [
        (format!("src/bin/day{day}.rs"), binding.as_bytes(), "module"),
        (format!("data/day{day}/input.txt"), b"", "input"),
        (format!("data/day{day}/example.txt"), b"", "example"),
    ];

    for (path, content, description) in paths {
        if let Err(e) = create_and_write_file(&path, content, overwrite) {
            eprintln!("Failed to create {description} file \"{}\": {e}", path);
            process::exit(1);
        }
        println!("Create {} file \"{}\"", description, path);
    }

    println!("---");
    println!("🎄 Type `cargo solve {day}` to run your solution.")
}

fn create_and_write_file(
    path: &str,
    content: &[u8],
    overwrite: bool,
) -> Result<(), std::io::Error> {
    let mut file = safe_create_file(path, overwrite)?;
    file.write_all(content)?;
    Ok(())
}
