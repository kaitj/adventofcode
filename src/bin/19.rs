use std::collections::HashMap;

adventofcode::solution!(19);

fn parse(input: &str) -> (Vec<&str>, Vec<&str>) {
    let (patterns, designs) = input.split_once("\n\n").unwrap();
    (patterns.split(", ").collect(), designs.lines().collect())
}

fn count_valid_patterns(
    pattern: &str,
    valid: &Vec<&str>,
    computed: &mut HashMap<String, usize>,
    max_len: usize,
) -> usize {
    if let Some(&result) = computed.get(pattern) {
        return result;
    }

    if pattern.is_empty() {
        return 1;
    }

    let mut combinations = 0;
    for i in 1..=max_len.min(pattern.len()) {
        if valid.contains(&&pattern[..i]) {
            let subcount = count_valid_patterns(&pattern[i..], valid, computed, max_len);
            combinations += subcount;
        }
    }
    computed.insert(pattern.to_string(), combinations);
    combinations
}

pub fn part_one(input: &str) -> Option<usize> {
    let (patterns, designs) = parse(input);
    let max_len = designs.iter().map(|v| v.len()).max().unwrap();
    let mut computed = HashMap::new();
    Some(
        designs
            .iter()
            .filter(|design| count_valid_patterns(design, &patterns, &mut computed, max_len) > 0)
            .count(),
    )
}

pub fn part_two(input: &str) -> Option<usize> {
    let (patterns, designs) = parse(input);
    let max_len = designs.iter().map(|v| v.len()).max().unwrap();
    let mut computed = HashMap::new();
    Some(
        designs
            .iter()
            .map(|design| count_valid_patterns(design, &patterns, &mut computed, max_len))
            .sum(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(6));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(16));
    }
}
