use adventofcode::{Direction, Matrix, Point};

adventofcode::solution!(15);

fn parse(input: &str) -> (Matrix<char>, Point, Vec<Direction>) {
    let (warehouse_map, moves) = input.split_once("\n\n").unwrap();

    let mut robot_pos = Point { x: 0, y: 0 };

    let cells: Vec<Vec<char>> = warehouse_map
        .lines()
        .map(|line| line.chars().collect())
        .collect();
    let warehouse = Matrix::from(cells);

    for y in 0..warehouse.rows {
        for x in 0..warehouse.cols {
            if warehouse.cells[y][x] == '@' {
                robot_pos = Point {
                    x: x as isize,
                    y: y as isize,
                };
                break;
            }
        }
    }

    let moves = moves
        .chars()
        .filter_map(|c| match c {
            '<' => Some(Direction::W),
            '>' => Some(Direction::E),
            '^' => Some(Direction::N),
            'v' => Some(Direction::S),
            _ => None,
        })
        .collect();

    (warehouse, robot_pos, moves)
}

fn push_stack(warehouse: &mut Matrix<char>, pos: Point, direction: Direction) -> bool {
    let next_pos = pos.neighbour(direction);

    // Check if next position is within bounds
    if !warehouse.point_inside(&next_pos) {
        return false;
    }

    match warehouse.get(&next_pos) {
        '.' => {
            // Move the box into the next open space
            warehouse.cells[next_pos.y as usize][next_pos.x as usize] = 'O';
            warehouse.cells[pos.y as usize][pos.x as usize] = '.';
            true
        }
        'O' => {
            // Attempt to push the next box recursively
            if push_stack(warehouse, next_pos, direction) {
                warehouse.cells[next_pos.y as usize][next_pos.x as usize] = 'O';
                warehouse.cells[pos.y as usize][pos.x as usize] = '.';
                true
            } else {
                false
            }
        }
        _ => false, // Wall or invalid tile; cannot push
    }
}

pub fn simulate_warehouse(
    mut warehouse: Matrix<char>,
    mut robot_pos: Point,
    moves: Vec<Direction>,
) -> usize {
    for direction in moves {
        let next_pos = robot_pos.neighbour(direction);

        if warehouse.point_inside(&next_pos) {
            match warehouse.get(&next_pos) {
                '.' => {
                    // Move the robot
                    warehouse.cells[robot_pos.y as usize][robot_pos.x as usize] = '.';
                    warehouse.cells[next_pos.y as usize][next_pos.x as usize] = '@';
                    robot_pos = next_pos;
                }
                'O' => {
                    // Attempt to push the box or stack
                    let box_pos = next_pos.neighbour(direction);
                    if push_stack(&mut warehouse, next_pos, direction) {
                        // Move the robot into the box's original position
                        warehouse.cells[robot_pos.y as usize][robot_pos.x as usize] = '.';
                        warehouse.cells[next_pos.y as usize][next_pos.x as usize] = '@';
                        robot_pos = next_pos;
                    }
                }
                _ => {
                    // Wall or invalid tile, do nothing
                }
            }
        }
    }

    calculate_gps(&warehouse)
}

fn calculate_gps(warehouse: &Matrix<char>) -> usize {
    let mut gps_sum = 0;

    for y in 0..warehouse.rows {
        for x in 0..warehouse.cols {
            if warehouse.cells[y][x] == 'O' {
                gps_sum += 100 * y + x;
            }
        }
    }
    gps_sum
}

pub fn part_one(input: &str) -> Option<usize> {
    let (warehouse, robot_pos, moves) = parse(input);
    Some(simulate_warehouse(warehouse, robot_pos, moves))
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
        assert_eq!(result, Some(10092));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
