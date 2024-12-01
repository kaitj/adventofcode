use std::collections::HashMap;

adventofcode::solution!(01);

pub fn parse_input(input: &str) -> (Vec<u32>, Vec<u32>) {
    input
        .lines()
        .filter_map(|line| {
            let mut ids = line.split_whitespace().map(str::parse::<u32>);
            match (ids.next(), ids.next()) {
                (Some(Ok(left)), Some(Ok(right))) => Some((left, right)),
                _ => None, // Skip invalid lines
            }
        })
        .unzip()
}

pub fn part_one(input: &str) -> Option<u32> {
    let (mut left, mut right) = parse_input(input);
    left.sort_unstable();
    right.sort_unstable();

    Some(
        left.iter()
            .zip(right.iter())
            .map(|(a, b)| a.abs_diff(*b))
            .sum(),
    )
}

pub fn part_two(input: &str) -> Option<u32> {
    let (left, right) = parse_input(input);

    let counts = right.into_iter().fold(HashMap::new(), |mut acc, val| {
        *acc.entry(val).or_insert(0) += 1;
        acc
    });

    Some(
        left.into_iter()
            .map(|x| x * counts.get(&x).copied().unwrap_or(0))
            .sum(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(11));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(31));
    }
}
