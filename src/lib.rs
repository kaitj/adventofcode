pub mod template;

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct Point {
    pub x: isize,
    pub y: isize,
}

impl Point {
    #[inline(always)]
    pub fn neighbour(&self, direction: Direction) -> Point {
        match direction {
            Direction::N => Point {
                x: self.x,
                y: self.y - 1,
            },
            Direction::E => Point {
                x: self.x + 1,
                y: self.y,
            },
            Direction::S => Point {
                x: self.x,
                y: self.y + 1,
            },
            Direction::W => Point {
                x: self.x - 1,
                y: self.y,
            },
            Direction::NE => Point {
                x: self.x + 1,
                y: self.y - 1,
            },
            Direction::NW => Point {
                x: self.x - 1,
                y: self.y - 1,
            },
            Direction::SE => Point {
                x: self.x + 1,
                y: self.y + 1,
            },
            Direction::SW => Point {
                x: self.x - 1,
                y: self.y + 1,
            },
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Direction {
    N,
    E,
    S,
    W,
    NE,
    SE,
    SW,
    NW,
}

pub const CARDINALS: [Direction; 4] = [Direction::N, Direction::E, Direction::S, Direction::W];

impl Direction {
    pub fn rotate_clockwise(&self) -> Direction {
        match self {
            Direction::N => Direction::E,
            Direction::E => Direction::S,
            Direction::S => Direction::W,
            Direction::W => Direction::N,
            Direction::NW => Direction::NE,
            Direction::NE => Direction::SE,
            Direction::SE => Direction::SW,
            Direction::SW => Direction::NW,
        }
    }
}

pub struct Matrix<T> {
    pub cells: Vec<Vec<T>>,
    pub cols: usize,
    pub rows: usize,
}

impl<T> From<Vec<Vec<T>>> for Matrix<T> {
    fn from(cells: Vec<Vec<T>>) -> Self {
        let rows = cells.len();
        let cols = cells[0].len();
        Self { cells, rows, cols }
    }
}

impl<T: Copy> Matrix<T> {
    pub fn get(&self, point: &Point) -> T {
        self.cells[point.y as usize][point.x as usize]
    }

    pub fn point_inside(&self, point: &Point) -> bool {
        point.x >= 0 && point.x < self.cols as isize && point.y >= 0 && point.y < self.rows as isize
    }

    pub fn neighbour(&self, point: &Point, direction: Direction) -> Option<Point> {
        let neighbour = point.neighbour(direction);

        if self.point_inside(&neighbour) {
            Some(neighbour)
        } else {
            None
        }
    }
}
