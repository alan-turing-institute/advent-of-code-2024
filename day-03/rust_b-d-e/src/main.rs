use std::env;
use std::fs;
use regex::Regex;

fn main() {
    // read in the file

    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    println!("Part one: {:?}", part_one(&contents));
    println!("Part two: {:?}", part_two(&contents));
}

fn part_one(input: &str) -> i32 {
    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();

    re.captures_iter(input)
        .map(|cap| {
            let x: i32 = cap[1].parse().unwrap();
            let y: i32 = cap[2].parse().unwrap();
            x * y
        })
        .sum()
}


enum Operation {
    StateChange(bool),
    Multiply(i32),
}

fn part_two(input: &str) -> i32 {
    // get all the multiplications
    let mul_re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    // get all the dos and don'ts (state changes)
    let state_re = Regex::new(r"do\(\)|don't\(\)").unwrap();

    // track positions
    let mut operations = Vec::new();

    // Get all multiplications and their positions
    // captures_iter built into regex crate - returns an iterator over all captures
    for capture in mul_re.captures_iter(input) {
        let pos = capture.get(0).unwrap().start();
        let x: i32 = capture[1].parse().unwrap();
        let y: i32 = capture[2].parse().unwrap();
        operations.push((pos, Operation::Multiply(x * y)));
    }

    // Get all state changes and their positions
    for matched in state_re.find_iter(input) {
        let enabled = matched.as_str() == "do()"; // true if "do()", false if "don't()"
        operations.push((matched.start(), Operation::StateChange(enabled)));
    }

    // Sort operations by position
    // currently sequence of multiplications and then state changes
    // we want to process them in order combined
    operations.sort_by_key(|&(pos, _)| pos);

    // Process operations in order
    let mut sum = 0;
    let mut enabled = true;  // Start enabled

    for (_, op) in operations {
        match op {
            // If we get a state change, update the tracked state
            Operation::StateChange(new_state) => enabled = new_state,
            // If we get a multiplication, add it to the sum IF enabled
            Operation::Multiply(result) if enabled => sum += result,
            _ => {}
        }
    }

    sum
}