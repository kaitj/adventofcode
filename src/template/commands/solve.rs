use std::process::{Command, Stdio};

use crate::template::Day;

pub fn handle(day: Day, release: bool, dhat: bool, submit_part: Option<u8>) {
    let cmd_args = build_cargo_args(day, release, dhat, submit_part);

    let status = Command::new("cargo")
        .args(&cmd_args)
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status()
        .expect("Failed to execute cargo command");

    if !status.success() {
        eprintln!("Cargo command failed with status: {:?}", status.code());
        std::process::exit(1);
    }
}

fn build_cargo_args(day: Day, release: bool, dhat: bool, submit_part: Option<u8>) -> Vec<String> {
    let mut args = vec!["run".to_string(), "--bin".to_string(), day.to_string()];

    if dhat {
        args.extend([
            "--profile".to_string(),
            "dhat".to_string(),
            "--features".to_string(),
            "dhat-heap".to_string(),
        ]);
    } else if release {
        args.push("--release".to_string());
    }

    args.push("--".to_string());

    if let Some(part) = submit_part {
        args.extend(["--submit".to_string(), part.to_string()]);
    }

    args
}
