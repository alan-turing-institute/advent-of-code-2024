use std::env;
use std::fs;

fn main() {

    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let puzzles = parse_file(&contents);

    // PART ONE

    let mut part_one = 0;
    for puzzle in &puzzles {
        part_one += attempt_puzzle_linalg(puzzle);
    }
    println!("Part one: {}", part_one);

    // PART TWO - same, but add 10000000000000 to every prize x and y
    let mut part_two = 0;

    for puzzle in &puzzles {
        let mut new_puzzle = puzzle.clone();
        new_puzzle.prize_x = Some(puzzle.prize_x.unwrap() + 10000000000000);
        new_puzzle.prize_y = Some(puzzle.prize_y.unwrap() + 10000000000000);
        part_two += attempt_puzzle_linalg(&new_puzzle);
    }

    println!("Part two: {}", part_two);
}

#[derive(Debug, Clone)]
struct Puzzle {
    a_x_delta: Option<i64>,
    a_y_delta: Option<i64>,
    b_x_delta: Option<i64>,
    b_y_delta: Option<i64>,
    prize_x: Option<i64>,
    prize_y: Option<i64>,
}

fn parse_line(delta_str: &str, op: char) -> (i64, i64) {
    // string of form: Button A: X+94, Y+34
    let parts: Vec<&str> = delta_str.split(", ").collect();
    let x_str = parts[0].split(op).collect::<Vec<&str>>()[1];
    let y_str = parts[1].split(op).collect::<Vec<&str>>()[1];
    (x_str.parse().unwrap(), y_str.parse().unwrap())
}

fn parse_file(contents: &str) -> Vec<Puzzle> {
    let mut puzzles = Vec::new();

    // split contents on "\n\n" into separate puzzle strings
    for puzzle_str in contents.split("\n\n") {
        // puzzle of form:
            // Button A: X+94, Y+34
            // Button B: X+22, Y+67
            // Prize: X=8400, Y=5400
        let lines = puzzle_str.split("\n");
        let mut new_puzzle = Puzzle {
            a_x_delta: None,
            a_y_delta: None,
            b_x_delta: None,
            b_y_delta: None,
            prize_x: None,
            prize_y: None,
        };
        for line in lines {
            let op = if line.contains("+") { '+' } else { '=' };
            let (x, y) = parse_line(line, op);
            if line.contains("A") {
                new_puzzle.a_x_delta = Some(x);
                new_puzzle.a_y_delta = Some(y);
            } else if line.contains("B") {
                new_puzzle.b_x_delta = Some(x);
                new_puzzle.b_y_delta = Some(y);
            } else if line.contains("Prize") {
                new_puzzle.prize_x = Some(x);
                new_puzzle.prize_y = Some(y);
            } else {
                panic!("Invalid line: {}", line);
            }
        }
        puzzles.push(new_puzzle);
    }
    puzzles
}


fn attempt_puzzle_linalg(puzzle: &Puzzle) -> i64 {
    const A_COST: i64 = 3;
    const B_COST: i64 = 1;

    let a_x = puzzle.a_x_delta.unwrap();
    let a_y = puzzle.a_y_delta.unwrap();
    let b_x = puzzle.b_x_delta.unwrap();
    let b_y = puzzle.b_y_delta.unwrap();
    let prize_x = puzzle.prize_x.unwrap();
    let prize_y = puzzle.prize_y.unwrap();

    // We have two equations:
    // a_x * A + b_x * B = prize_x
    // a_y * A + b_y * B = prize_y

    let determinant = a_x * b_y - b_x * a_y;
    // If determinant is 0, equations are either parallel or identical - no solution is possible
    if determinant == 0 {
        return 0;
    }

    // Calculate A and B
    let a = (prize_x * b_y - b_x * prize_y) as f64 / determinant as f64;
    let b = (a_x * prize_y - prize_x * a_y) as f64 / determinant as f64;

    // Check if we have positive integer solutions
    if a.fract() != 0.0 || b.fract() != 0.0 || a < 0.0 || b < 0.0 {
        return 0;
    }

    let a_int = a as i64;
    let b_int = b as i64;

    // Verify the solution
    if a_x * a_int + b_x * b_int != prize_x ||
       a_y * a_int + b_y * b_int != prize_y {
        return 0;
    }

    // Calculate and return the cost
    a_int * A_COST + b_int * B_COST
}