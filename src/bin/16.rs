use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashSet};

use adventofcode::{Direction, Matrix, Point};

adventofcode::solution!(16);

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
struct State {
    point: Point,
    direction: Direction,
    score: u64,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.score.cmp(&self.score)
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn solve_maze(
    matrix: &Matrix<char>,
    start: Point,
    end: Point,
    start_direction: Direction,
) -> Option<u64> {
    let mut visited = HashSet::new();
    let mut heap = BinaryHeap::new();

    // Initial state
    heap.push(State {
        point: start,
        direction: start_direction,
        score: 0,
    });

    while let Some(current) = heap.pop() {
        // Reached end
        if current.point == end {
            return Some(current.score);
        }

        // Create unique key
        let state_key = (current.point, current.direction);
        if visited.contains(&state_key) {
            continue;
        }
        visited.insert(state_key);

        // Try moving forward
        if let Some(forward) = matrix.neighbour(&current.point, current.direction) {
            if is_valid_move(matrix, &forward) {
                heap.push(State {
                    point: forward,
                    direction: current.direction,
                    score: current.score + 1,
                });
            }
        }

        // Try rotating clockwise
        let clockwise = current.direction.rotate_clockwise();
        heap.push(State {
            point: current.point,
            direction: clockwise,
            score: current.score + 1000,
        });

        let counter_clickwise = current.direction.rotate_counterclockwise();
        heap.push(State {
            point: current.point,
            direction: counter_clickwise,
            score: current.score + 1000,
        });
    }
    None
}

fn is_valid_move(matrix: &Matrix<char>, point: &Point) -> bool {
    matrix.point_inside(point) && matrix.get(point) != '#'
}

fn parse_matrix(input: &str) -> Matrix<char> {
    let cells: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();
    Matrix::from(cells)
}

fn find_point(matrix: &Matrix<char>, target: char) -> Option<Point> {
    for y in 0..matrix.rows {
        for x in 0..matrix.cols {
            let point = Point {
                x: x as isize,
                y: y as isize,
            };
            if matrix.get(&point) == target {
                return Some(point);
            }
        }
    }
    None
}

pub fn part_one(input: &str) -> Option<u64> {
    let matrix = parse_matrix(input);
    let start_point = find_point(&matrix, 'S')?;
    let end_point = find_point(&matrix, 'E')?;

    solve_maze(&matrix, start_point, end_point, Direction::E)
}

pub fn part_two(input: &str) -> Option<u32> {
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(7036));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
