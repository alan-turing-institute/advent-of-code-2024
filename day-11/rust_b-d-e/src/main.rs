use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    // split into vec of nums based on spaces
    let mut stones: Vec<i64> = contents
        .split_whitespace()
        .map(|s| s.parse().expect("parse error"))
        .collect();

    println!("Input stones:");
    println!("{:?}", stones);

    println!("Part one: {}", part_one(&mut stones));
}


fn blink(stones: &mut Vec<i64>) -> Vec<i64> {
    // for each stone:
        // If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        // If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
        // If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.

    let mut new_stones = Vec::new();
    for i in 0..stones.len() {
        let stone = stones[i];
        if stone == 0 {
            new_stones.push(1);
        } else if stone.to_string().len() % 2 == 0 {
            let stone_str = stone.to_string();
            let half = stone_str.len() / 2;
            let left = stone_str[..half].parse().expect("parse error");
            let right = stone_str[half..].parse().expect("parse error");
            new_stones.push(left);
            new_stones.push(right);
        } else {
            new_stones.push(stone * 2024);
        }
    }

    new_stones
}

fn part_one(stones: &mut Vec<i64>) -> usize {

    let num_blinks: i8 = 75;

    for _ in 0..num_blinks {
        *stones = blink(stones);
        // println!("{:?}", stones);
    }

    stones.len()
}