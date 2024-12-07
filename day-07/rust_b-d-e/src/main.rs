use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut input: Vec<(i64, Vec<i64>)> = Vec::new();

    for line in contents.lines() {
        let mut parts = line.split(": ");
        let result = parts.next().unwrap().parse::<i64>().unwrap();
        let operands = parts.next().unwrap().split(" ").map(|x| x.parse::<i64>().unwrap()).collect();
        input.push((result, operands));
    }

    println!("Part one: {}", part_one(&input));
    println!("Part two: {}", part_two(&input));
}

fn part_one(input: &[(i64, Vec<i64>)]) -> i64 {
    let mut sum = 0;

    for (target, operands) in input {
        if valid_equation_exists(*target, operands, operands.len() - 1, false) {
            sum += target;
        }
    }

    sum
}

fn part_two(input: &[(i64, Vec<i64>)]) -> i64 {
    let mut sum = 0;

    // same thing, but now can also have operator | which concatonates the numbers
    for (target, operands) in input {
        if valid_equation_exists(*target, operands, operands.len() - 1, true) {
            sum += target;
        }
    }

    sum
}


fn valid_equation_exists(target: i64, operands: &[i64], index: usize, concat: bool) -> bool {
    // Base case: if we're at the first number, check if we've reached it
    if index == 0 {
        return target == operands[0];
    }

    // Try each possible operation working backwards

    // Addition: if result was a + b, then a = result - b
    if target >= operands[index] &&
       valid_equation_exists(target - operands[index], operands, index - 1, concat) {
        return true;
    }

    // Multiplication: if result was a * b, then a = result / b
    if target % operands[index] == 0 &&
    valid_equation_exists(target / operands[index], operands, index - 1, concat) {
        return true;
    }

    // Concatenation: if result ends with b, then a is result/10^(digits in b)
    if concat {
        // Check if test_value ends with current term
        let power = closest_power_of_ten(operands[index]);
        if target % power == operands[index] {
            // If it does, divide by appropriate power of 10 to get the left part
            if valid_equation_exists(target / power, operands, index - 1, concat) {
                return true;
            }
        }
    }

    false // cannot find a valid solution
}

fn closest_power_of_ten(n: i64) -> i64 {
    10_i64.pow((n.ilog10() + 1) as u32)
}