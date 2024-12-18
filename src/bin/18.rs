use adventofcode::{Point, CARDINALS};
use std::collections::{HashMap, HashSet, VecDeque};

adventofcode::solution!(18);

fn parse(input: &str) -> Vec<Point> {
    input
        .lines()
        .map(|line| {
            let (x, y) = line.split_once(',').unwrap();
            Point {
                x: x.parse::<isize>().unwrap(),
                y: y.parse::<isize>().unwrap(),
            }
        })
        .collect::<Vec<Point>>()
}

fn shortest_path(corrupted: &Vec<Point>, exit: Point, bytes: usize) -> Option<usize> {
    let corrupted: HashSet<_> = corrupted.iter().take(bytes).collect();
    let start = Point { x: 0, y: 0 };

    let mut queue = VecDeque::from([(start, 0)]);
    let mut visited = HashSet::from([start]);

    while let Some((position, distance)) = queue.pop_front() {
        for direction in CARDINALS {
            let next_position = position.neighbour(direction);

            if next_position.x >= 0
                && next_position.x <= exit.x
                && next_position.y >= 0
                && next_position.y <= exit.y
            {
                if next_position == exit {
                    return Some(distance + 1);
                }

                if !corrupted.contains(&next_position) && !visited.contains(&next_position) {
                    queue.push_back((next_position, distance + 1));
                    visited.insert(next_position);
                }
            }
        }
    }
    None
}

fn blocking_byte(corrupted: &Vec<Point>, exit: Point) -> Option<Point> {
    let byte_idxes =
        corrupted
            .iter()
            .enumerate()
            .fold(HashMap::new(), |mut idxes, (index, location)| {
                idxes.entry(location).or_insert(index);
                idxes
            });

    let start = Point { x: 0, y: 0 };
    let starting_idx = if let Some(index) = byte_idxes.get(&start) {
        *index
    } else {
        corrupted.len()
    };

    let mut queue = VecDeque::from([(start, starting_idx)]);
    let mut visited = HashMap::from([(start, starting_idx)]);
    let mut blocking_byte = None;
    let mut max_index = 0;

    while let Some((position, index)) = queue.pop_front() {
        for direction in CARDINALS {
            let next_position = position.neighbour(direction);

            if next_position.x >= 0
                && next_position.x <= exit.x
                && next_position.y >= 0
                && next_position.y <= exit.y
            {
                if next_position == exit && index >= max_index && index < corrupted.len() {
                    blocking_byte = Some(corrupted[index]);
                    max_index = index;
                }

                if let Some(prev_index) = visited.get(&next_position) {
                    if *prev_index >= index {
                        continue;
                    }
                }

                match byte_idxes.get(&next_position) {
                    Some(corrupted_idx) if *corrupted_idx < index => {
                        let new_idx = *corrupted_idx;

                        queue.push_back((next_position, new_idx));
                        visited.insert(next_position, new_idx);
                    }
                    _ => {
                        queue.push_back((next_position, index));
                        visited.insert(next_position, index);
                    }
                }
            }
        }
    }
    blocking_byte
}

pub fn part_one(input: &str) -> Option<usize> {
    let corrupted = parse(input);
    let exit = Point { x: 70, y: 70 };
    let bytes = 1024;
    shortest_path(&corrupted, exit, bytes)
}

pub fn part_two(input: &str) -> Option<String> {
    let corrupted = parse(input);
    let exit = Point { x: 70, y: 70 };
    let blocking = blocking_byte(&corrupted, exit).unwrap();
    Some(format!("{},{}", blocking.x, blocking.y))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        // Starting Point<(0, 0)>; End Point<(6, 6)>
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(22));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some("6,1".to_string()));
    }
}
