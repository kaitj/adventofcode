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
