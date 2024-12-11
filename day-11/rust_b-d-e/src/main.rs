use std::env;
use std::fs;
use std::collections::BTreeMap;

type Counter = BTreeMap<i64, i64>;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let stones: Vec<i64> = contents
        .split_whitespace()
        .map(|s| s.parse().expect("parse error"))
        .collect();

    println!("Input stones:");
    println!("{:?}", stones);

    println!("Part one: {}", solve(&stones, 25));
    println!("Part two: {}", solve(&stones, 75));
}

fn count(stones: &[i64]) -> Counter {
    let mut counter = Counter::new();
    for &stone in stones {
        *counter.entry(stone).or_insert(0) += 1;
    }
    counter
}

fn count_digits(mut n: i64) -> u32 {
    let mut count = 0;
    while n > 0 {
        n /= 10;
        count += 1;
    }
    count
}

fn split_number(n: i64, digits: u32) -> (i64, i64) {
    let half_digits = digits / 2;
    let divisor = 10_i64.pow(half_digits);
    let right = n % divisor;
    let left = n / divisor;
    (left, right)
}

// Returns Vec of (new_stone, count) pairs
fn blink_single(stone: i64) -> Vec<(i64, i64)> {
    if stone == 0 {
        vec![(1, 1)]
    } else {
        let digit_count = count_digits(stone);
        if digit_count % 2 == 0 {
            let (left, right) = split_number(stone, digit_count);
            vec![(left, 1), (right, 1)]
        } else {
            vec![(stone * 2024, 1)]
        }
    }
}

fn blink_with_count(pair: (i64, i64)) -> Vec<(i64, i64)> {
    let (stone, count) = pair;
    blink_single(stone).into_iter()
        .map(|(new_stone, multiplier)| (new_stone, multiplier * count))
        .collect()
}

fn iterate_blink(counter: Counter) -> Counter {
    let mut new_counter = Counter::new();
    for (stone, count) in counter {
        for (new_stone, new_count) in blink_with_count((stone, count)) {
            *new_counter.entry(new_stone).or_insert(0) += new_count;
        }
    }
    new_counter
}

fn solve(stones: &[i64], n: usize) -> i64 {
    let mut current = count(stones);
    for _ in 0..n {
        current = iterate_blink(current);
    }
    current.values().sum()
}