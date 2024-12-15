use adventofcode::{Matrix, Point, CARDINALS};
use std::collections::HashSet;

adventofcode::solution!(12);

struct Grid {
    plants: Matrix<char>,
}

fn parse(input: &str) -> Grid {
    let cells: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();

    Grid {
        plants: Matrix::from(cells),
    }
}

fn process_plant(
    grid: &Grid,
    visited: &mut HashSet<Point>,
    start: Point,
    part_two: bool,
) -> (usize, usize) {
    let mut stack = vec![start];
    let mut area = 0;
    let mut perimeter = 0;
    let mut edges: HashSet<(Point, Point)> = HashSet::new();
    let plant_type = grid.plants.get(&start);

    while let Some(point) = stack.pop() {
        if visited.contains(&point) {
            continue;
        }

        visited.insert(point);
        area += 1;
        let mut local_perimeter = 4;

        for &direction in &CARDINALS {
            if let Some(neighbour) = grid.plants.neighbour(&point, direction) {
                if grid.plants.get(&neighbour) == plant_type {
                    local_perimeter -= 1;
                    if !visited.contains(&neighbour) {
                        stack.push(neighbour);
                    }
                } else {
                    // Edge inside of grid
                    let edge = (point, neighbour);
                    edges.insert(edge);
                }
            } else {
                // Edge outside of grid
                let edge = (point, point);
                edges.insert(edge);
            }
        }
        perimeter += local_perimeter;
    }

    if part_two {
        (area, edges.len())
    } else {
        (area, perimeter)
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    let grid = parse(input);
    let mut visited = HashSet::new();
    let mut total_price = 0;

    for y in 0..grid.plants.rows {
        for x in 0..grid.plants.cols {
            let point = Point {
                x: x as isize,
                y: y as isize,
            };

            if !visited.contains(&point) {
                let (area, perimeter) = process_plant(&grid, &mut visited, point, false);
                total_price += area * perimeter;
            }
        }
    }

    Some(total_price as u32)
}

pub fn part_two(input: &str) -> Option<u32> {
    let grid = parse(input);
    let mut visited = HashSet::new();
    let mut total_price = 0;

    for y in 0..grid.plants.rows {
        for x in 0..grid.plants.cols {
            let point = Point {
                x: x as isize,
                y: y as isize,
            };

            if !visited.contains(&point) {
                let (area, sides) = process_plant(&grid, &mut visited, point, true);
                total_price += area * sides;
            }
        }
    }

    Some(total_price as u32)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(1930));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(1206));
    }
}
