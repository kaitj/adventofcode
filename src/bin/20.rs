use adventofcode::{Point, CARDINALS};
use std::collections::{HashMap, HashSet};

adventofcode::solution!(20);

const SAVED: i32 = 100;

#[derive(Debug)]
struct RaceSetup {
    obstacles: HashSet<Point>,
    start: Point,
    end: Point,
}

fn parse(input: &str) -> RaceSetup {
    let mut start = Point::new(0, 0);
    let mut end = Point::new(0, 0);
    let mut obstacles: HashSet<Point> = HashSet::new();

    input.lines().enumerate().for_each(|(y, row)| {
        row.chars().enumerate().for_each(|(x, ch)| match ch {
            '#' => {
                obstacles.insert(Point::new(x as isize, y as isize));
            }
            'S' => {
                start = Point::new(x as isize, y as isize);
            }
            'E' => {
                end = Point::new(x as isize, y as isize);
            }
            _ => {}
        })
    });

    RaceSetup {
        obstacles,
        start,
        end,
    }
}

pub fn part_one(input: &str) -> Option<isize> {
    let race_setup = parse(input);
    let mut path = HashMap::from([(race_setup.start, 0)]);
    let mut position = race_setup.start;

    while position != race_setup.end {
        for direction in CARDINALS {
            let next_position = position.neighbour(direction);

            // If haven't visited yet
            if !path.contains_key(&next_position) && !race_setup.obstacles.contains(&next_position)
            {
                path.insert(next_position, *path.get(&position).unwrap() + 1);
                position = next_position;
            }
        }
    }

    let mut count = 0;
    for (position, cost) in path.iter() {
        for next_position in [
            Point::new(position.x - 2, position.y),
            Point::new(position.x + 2, position.y),
            Point::new(position.x, position.y - 2),
            Point::new(position.x, position.y + 2),
        ] {
            if let Some(next_cost) = path.get(&next_position) {
                if next_cost - cost >= SAVED + 2 {
                    count += 1;
                }
            }
        }
    }

    Some(count)
}

pub fn part_two(input: &str) -> Option<isize> {
    let race_setup = parse(input);
    let mut path = vec![race_setup.start];
    let mut visited = HashSet::from([race_setup.start]);
    let mut position = race_setup.start;

    while position != race_setup.end {
        for direction in CARDINALS {
            let next_position = position.neighbour(direction);

            // If haven't visited yet
            if !visited.contains(&next_position) && !race_setup.obstacles.contains(&next_position) {
                visited.insert(next_position);
                path.push(next_position);
                position = next_position;
            }
        }
    }

    let mut count = 0;
    for start_idx in 0..path.len() {
        for end_idx in start_idx + 1..path.len() {
            let distance = path[start_idx].manhattan(&path[end_idx]);

            if distance <= 20 && (end_idx - start_idx) as i32 >= SAVED + distance as i32 {
                count += 1;
            }
        }
    }

    Some(count)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
