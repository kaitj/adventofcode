use itertools::Itertools;

adventofcode::solution!(14);

struct Robot {
    p: (isize, isize),
    v: (isize, isize),
}

impl From<&str> for Robot {
    fn from(line: &str) -> Self {
        let (pos, velocity) = line[2..].split_once(" v=").unwrap();
        let (px, py) = pos.split_once(',').unwrap();
        let (vx, vy) = velocity.split_once(',').unwrap();

        Self {
            p: (px.parse().unwrap(), py.parse().unwrap()),
            v: (vx.parse().unwrap(), vy.parse().unwrap()),
        }
    }
}

impl Robot {
    /// Predict position after T seconds
    fn predict(&mut self, secs: isize) {
        self.p.0 = (self.p.0 + self.v.0 * secs).rem_euclid(WIDTH);
        self.p.1 = (self.p.1 + self.v.1 * secs).rem_euclid(HEIGHT);
    }

    /// Check if robot is exactly in the middle
    fn safe(&self) -> bool {
        self.p.0 != WIDTH / 2 && self.p.1 != HEIGHT / 2
    }

    /// Determine quadrant robot is in;
    fn quadrant(&self) -> usize {
        if self.p.0 < WIDTH / 2 {
            if self.p.1 < HEIGHT / 2 {
                return 0;
            }
            return 1;
        } else if self.p.1 < HEIGHT / 2 {
            return 2;
        }
        3
    }
}

// Example is (11, 17)
const WIDTH: isize = 101;
const HEIGHT: isize = 103;

pub fn part_one(input: &str) -> Option<isize> {
    let mut quadrants = vec![0; 4];

    input.lines().for_each(|line| {
        let mut robot = Robot::from(line);
        robot.predict(100);

        if robot.safe() {
            quadrants[robot.quadrant()] += 1;
        }
    });
    Some(quadrants.into_iter().product())
}

pub fn part_two(input: &str) -> Option<usize> {
    let mut pic: Vec<Robot> = input.lines().map(|line| Robot::from(line)).collect();
    Some(
        (1..=WIDTH as usize * HEIGHT as usize)
            .map(|t: usize| {
                (
                    t,
                    pic.iter_mut()
                        .map(|r| {
                            r.predict(1);
                            r.quadrant()
                        })
                        .counts()
                        .values()
                        .product::<usize>(),
                )
            })
            .min_by(|&x, &y| x.1.cmp(&y.1))
            .unwrap()
            .0,
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(12));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
