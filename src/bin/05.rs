use std::collections::HashMap;

adventofcode::solution!(5);

type Graph = HashMap<usize, Vec<usize>>;

fn parse(input: &str) -> Option<(Graph, Vec<Vec<usize>>)> {
    let (head, tail) = input.split_once("\n\n")?;

    let graph: Graph = head
        .split("\n")
        .filter_map(|line| {
            let (x, y) = line.split_once('|')?;
            Some((x.parse().ok()?, y.parse().ok()?))
        })
        .fold(HashMap::new(), |mut acc, (pre, post)| {
            acc.entry(post).or_default().push(pre);
            acc
        });

    let updates = tail
        .lines()
        .map(|line| line.split(',').filter_map(|s| s.parse().ok()).collect())
        .collect();

    Some((graph, updates))
}

fn validate_update(graph: &Graph, update: &[usize]) -> bool {
    for (i, x) in update.iter().enumerate() {
        let rest = &update[i..];

        if let Some(pre) = graph.get(x) {
            if rest.iter().any(|y| pre.contains(y)) {
                return false;
            }
        }
    }

    true
}

fn reorder_update(graph: &Graph, update: &[usize]) -> Vec<usize> {
    let mut sorted_update = update.to_vec();
    sorted_update.sort_by(|a, b| {
        if graph.get(a).map_or(false, |pre| pre.contains(b)) {
            std::cmp::Ordering::Greater
        } else if graph.get(b).map_or(false, |pre| pre.contains(a)) {
            std::cmp::Ordering::Less
        } else {
            std::cmp::Ordering::Equal
        }
    });
    sorted_update
}

pub fn part_one(input: &str) -> Option<usize> {
    let (graph, updates) = parse(input)?;
    Some(
        updates
            .into_iter()
            .filter(|update| validate_update(&graph, update))
            .map(|update| update[update.len() / 2])
            .sum(),
    )
}

pub fn part_two(input: &str) -> Option<usize> {
    let (graph, updates) = parse(input)?;
    Some(
        updates
            .into_iter()
            .filter_map(|update| {
                if !validate_update(&graph, &update) {
                    let reordered = reorder_update(&graph, &update);
                    Some(reordered[reordered.len() / 2])
                } else {
                    None
                }
            })
            .sum(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(143));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(123));
    }
}
