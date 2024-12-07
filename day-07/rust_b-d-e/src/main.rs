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
        if valid(*target, operands, operands.len() - 1, false) {
            sum += target;
        }
    }

    sum
}

fn part_two(input: &[(i64, Vec<i64>)]) -> i64 {
    let mut sum = 0;

    // same thing, but now can also have operator | which concatonates the numbers
    for (target, operands) in input {
        if valid(*target, operands, operands.len() - 1, true) {
            sum += target;
        }
    }

    sum
}


fn valid(test_value: i64, terms: &[i64], index: usize, concat: bool) -> bool {
    // Base case: if we're at the first number, check if we've reached it
    if index == 0 {
        return test_value == terms[0];
    }

    // Try each possible operation working backwards

    // Addition: if result was a + b, then a = result - b
    if test_value >= terms[index] &&
       valid(test_value - terms[index], terms, index - 1, concat) {
        return true;
    }

    // Multiplication: if result was a * b, then a = result / b
    if test_value % terms[index] == 0 &&
       valid(test_value / terms[index], terms, index - 1, concat) {
        return true;
    }

    // Concatenation: if result ends with b, then a is result/10^(digits in b)
    if concat {
        // Check if test_value ends with current term
        let power = next_power_of_ten(terms[index]);
        if test_value % power == terms[index] {
            // If it does, divide by appropriate power of 10 to get the left part
            if valid(test_value / power, terms, index - 1, concat) {
                return true;
            }
        }
    }

    false
}

fn next_power_of_ten(n: i64) -> i64 {
    // helper to work out magnitude of number concatonated
    if n < 10 {
        10
    } else if n < 100 {
        100
    } else if n < 1000 {
        1000
    }
    else {
        panic!("Unexpected number: {}", n);
    }
}