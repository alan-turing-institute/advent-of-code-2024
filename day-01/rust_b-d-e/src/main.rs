use std::env;
use std::fs;
use std::collections::HashMap;

fn main() {

    // part one

    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    // split into two arrays of ints based on columns
    let mut col1: Vec<i32> = Vec::new();
    let mut col2: Vec<i32> = Vec::new();
    for line in contents.lines() {
        let parts: Vec<&str> = line.split("   ").collect();
        col1.push(parts[0].parse().unwrap());
        col2.push(parts[1].parse().unwrap());
    }

    // sort the two columns
    col1.sort();
    col2.sort();

    // find absolute difference between the two columns
    let mut diff: Vec<i32> = Vec::new();
    for i in 0..col1.len() {
        diff.push((col1[i] - col2[i]).abs());
    }

    // find the sum of the differences
    let sum: i32 = diff.iter().sum();
    println!("Part One (sum of differences): {sum}");

    /////////////////////////////////////////////////

    // part two

    let mut similarity: i32 = 0; // running total

    // HashMap to count occurrences in col2
    // i32 (number) -> i32 (occurences)
    let mut num_counts: HashMap<i32, i32> = HashMap::new();
    // populate hashmap with counts from col2
    for &num in col2.iter() {
        // increment count for num, creating first if necessary
        *num_counts.entry(num).or_insert(0) += 1;
    }

    // iterate through col1 and multiply by counts from HashMap
    for &num in col1.iter() {
        // query hashmap. if not present, default to 0
        let count = num_counts.get(&num).unwrap_or(&0);
        // update similarity score
        similarity += num * count;
    }

    println!("Part Two (similarity score): {similarity}");
}