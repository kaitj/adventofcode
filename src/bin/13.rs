adventofcode::solution!(13);

struct Machine {
    a_x: i64,
    a_y: i64,
    b_x: i64,
    b_y: i64,
    p_x: i64,
    p_y: i64,
}

fn button_value(str: &str) -> Option<i64> {
    str.split_once('+').and_then(|n| n.1.parse().ok())
}

fn button(line: &str) -> Option<(i64, i64)> {
    let (x, y) = line.split_once(": ")?.1.split_once(", ")?;
    button_value(x).zip(button_value(y))
}

fn prize_value(str: &str) -> Option<i64> {
    str.split_once('=').and_then(|n| n.1.parse().ok())
}

fn prize(line: &str) -> Option<(i64, i64)> {
    let (x, y) = line.split_once(": ")?.1.split_once(", ")?;
    prize_value(x).zip(prize_value(y))
}

fn parse_machine(machine: &str) -> Option<Machine> {
    let mut lines = machine.lines();
    let (a_x, a_y) = button(lines.next()?)?;
    let (b_x, b_y) = button(lines.next()?)?;
    let (p_x, p_y) = prize(lines.next()?)?;
    Some(Machine {
        a_x,
        a_y,
        b_x,
        b_y,
        p_x,
        p_y,
    })
}

fn parse(input: &str) -> Vec<Machine> {
    input.split("\n\n").filter_map(parse_machine).collect()
}

fn solve(machine: &Machine) -> Option<i64> {
    let Machine = machine;

    let det = Machine.a_x * Machine.b_y - Machine.a_y * Machine.b_x;

    let x = (Machine.p_x * Machine.b_y - Machine.p_y * Machine.b_x) / det;
    let y = (Machine.p_y * Machine.a_x - Machine.p_x * Machine.a_y) / det;

    if x * Machine.a_x + y * Machine.b_x == Machine.p_x
        && x * Machine.a_y + y * Machine.b_y == Machine.p_y
    {
        Some(3 * x + y)
    } else {
        None
    }
}

pub fn part_one(input: &str) -> Option<i64> {
    let machines = parse(input);

    Some(
        machines
            .into_iter()
            .filter_map(|machine| solve(&machine))
            .sum(),
    )
}

pub fn part_two(input: &str) -> Option<i64> {
    let mut machines = parse(input);

    Some(
        machines
            .iter_mut()
            .filter_map(|machine| {
                machine.p_x += 10000000000000;
                machine.p_y += 10000000000000;
                solve(&machine)
            })
            .sum(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, Some(480));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&adventofcode::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
