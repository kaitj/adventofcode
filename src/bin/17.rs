adventofcode::solution!(17);

#[derive(Debug, Clone)]
struct Computer {
    program: Vec<u64>,
    ip: usize,
    a: u64,
    b: u64,
    c: u64,
}

impl Computer {
    fn run(&mut self) -> Option<u64> {
        while self.ip < self.program.len() {
            let combo = |index| match self.program[index] {
                0..4 => self.program[index],
                4 => self.a,
                5 => self.b,
                6 => self.c,
                _ => unreachable!(),
            };

            match self.program[self.ip] {
                0 => self.a >>= combo(self.ip + 1),
                1 => self.b ^= self.program[self.ip + 1],
                2 => self.b = combo(self.ip + 1) % 8,
                3 => {
                    if self.a != 0 {
                        self.ip = self.program[self.ip + 1] as usize;
                        continue;
                    }
                }
                4 => self.b ^= self.c,
                5 => {
                    let out = combo(self.ip + 1) % 8;
                    self.ip += 2;
                    return Some(out);
                }
                6 => self.b = self.a >> combo(self.ip + 1),
                7 => self.c = self.a >> combo(self.ip + 1),
                _ => unreachable!(),
            }

            self.ip += 2;
        }

        None
    }
}
fn parse(input: &str) -> Computer {
    let prog: Vec<u64> = input
        .lines()
        .filter_map(|line| line.split_once(':'))
        .flat_map(|(_, values)| values.split(','))
        .filter_map(|s| s.trim().parse::<u64>().ok())
        .collect();

    Computer {
        program: prog[3..].to_vec(),
        ip: 0,
        a: prog[0],
        b: prog[1],
        c: prog[2],
    }
}

pub fn part_one(input: &str) -> Option<String> {
    let mut computer = parse(input);
    let mut out = Vec::new();

    while let Some(n) = computer.run() {
        let digit = (n as u8 + b'0') as char;
        out.push(digit);
        out.push(',');
    }

    out.pop();
    Some(out.iter().collect())
}

pub fn part_two(input: &str) -> Option<u64> {
    let computer = parse(input);
    let mut valid = vec![0];

    for &out in computer.program.iter().rev() {
        let mut next = Vec::new();

        for v in valid {
            for n in 0..8 {
                let a = (v << 3) | n;
                let mut new_computer = computer.clone();
                new_computer.a = a;

                if let Some(result) = new_computer.run() {
                    if result == out {
                        next.push(a);
                    }
                }
            }
        }
        valid = next;
    }
    Some(*valid.iter().min().unwrap())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file_part("examples", DAY, 1));
        assert_eq!(result, Some("4,6,3,5,6,3,5,2,1,0".to_string()));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file_part("examples", DAY, 2));
        assert_eq!(result, Some(117440));
    }
}
