adventofcode::solution!(2);

fn parse(line: &str) -> Vec<u32> {
    line.split_ascii_whitespace()
        .filter_map(|v| v.parse().ok())
        .collect()
}

/// Validates values in a vector to be monotonically increasing or decreasing, with an
/// absolute difference of 1 <= x <= 3
fn validate(values: Vec<u32>, correct: bool) -> bool {
    let increasing = values[1] > values[0];

    let is_safe = values.windows(2).all(|pairs| {
        let a = pairs[0];
        let b = pairs[1];

        if (increasing && b <= a) || (!increasing && b >= a) {
            return false;
        }

        (1..=3).contains(&a.abs_diff(b))
    });

    if !is_safe && correct {
        (0..values.len())
            .map(|x| {
                let mut arr = values.clone();
                arr.remove(x);
                arr
            })
            .any(|v| validate(v, false))
    } else {
        is_safe
    }
}

pub fn part_one(_input: &str) -> Option<usize> {
    Some(
        _input
            .lines()
            .filter(|line| validate(parse(line), false))
            .count(),
    )
}

pub fn part_two(_input: &str) -> Option<usize> {
    Some(
        _input
            .lines()
            .filter(|line| validate(parse(line), true))
            .count(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(2));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(4));
    }
}
