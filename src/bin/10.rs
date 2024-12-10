use std::collections::HashSet;

use adventofcode::{Matrix, Point, CARDINALS};

adventofcode::solution!(10);

fn parse(input: &str) -> (Matrix<u32>, Vec<Point>) {
    let mut trailheads = vec![];

    let cells: Vec<Vec<u32>> = input
        .lines()
        .enumerate()
        .map(|(y, line)| {
            line.chars()
                .enumerate()
                .map(|(x, ch)| {
                    let val = ch.to_digit(10).unwrap();
                    if val == 0 {
                        trailheads.push(Point {
                            x: x as isize,
                            y: y as isize,
                        });
                    }
                    val
                })
                .collect()
        })
        .collect();

    (Matrix::from(cells), trailheads)
}

fn map_path(matrix: &Matrix<u32>, paths: Vec<Point>) -> Vec<Point> {
    paths
        .into_iter()
        .flat_map(|point| {
            let val = matrix.get(&point);
            if val == 9 {
                return vec![point];
            }

            let neighbours: Vec<Point> = CARDINALS
                .iter()
                .filter_map(|direction| {
                    let neighbour = matrix.neighbour(&point, *direction)?;
                    if matrix.get(&neighbour) == val + 1 {
                        Some(neighbour)
                    } else {
                        None
                    }
                })
                .collect();

            if neighbours.is_empty() {
                vec![]
            } else {
                map_path(matrix, neighbours)
            }
        })
        .collect()
}

pub fn part_one(input: &str) -> Option<usize> {
    let (matrix, trailheads) = parse(input);
    Some(
        trailheads
            .into_iter()
            .map(|trailhead| HashSet::<Point>::from_iter(map_path(&matrix, vec![trailhead])).len())
            .sum(),
    )
}

pub fn part_two(input: &str) -> Option<usize> {
    let (matrix, trailheads) = parse(input);
    Some(
        trailheads
            .into_iter()
            .map(|trailhead| map_path(&matrix, vec![trailhead]).len())
            .sum(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(36));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(81));
    }
}
