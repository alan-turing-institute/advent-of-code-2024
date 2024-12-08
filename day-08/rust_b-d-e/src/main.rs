use std::env;
use std::fs;
use std::collections::{HashMap, HashSet};

fn in_bounds(pos: (i32, i32), height: i32, width: i32) -> bool {
    pos.0 >= 0 && pos.1 >= 0 && pos.0 < height && pos.1 < width
}

fn main() {
    // Read input file
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let lines: Vec<&str> = contents.lines().collect();

    // Store antenna positions
    let mut antenna_positions: HashMap<char, Vec<(i32, i32)>> = HashMap::new();

    for (i, line) in lines.iter().enumerate() {
        for (j, freq) in line.chars().enumerate() {
            if freq != '.' {
                antenna_positions
                    .entry(freq)
                    .or_insert_with(Vec::new)
                    .push((i as i32, j as i32));
            }
        }
    }

    let height = lines.len() as i32;
    let width = lines[0].len() as i32;

    let mut antinodes_part1: Vec<(i32, i32)> = Vec::new();
    let mut antinodes_part2: Vec<(i32, i32)> = Vec::new();

    // Process each antenna type
    for positions in antenna_positions.values() {
        // Generate all combinations of positions
        for i in 0..positions.len() {
            for j in (i + 1)..positions.len() {
                let pos1 = positions[i];
                let pos2 = positions[j];

                let direction = (pos2.0 - pos1.0, pos2.1 - pos1.1);
                let mut an_plus = (pos2.0 + direction.0, pos2.1 + direction.1);
                let mut an_min = (pos1.0 - direction.0, pos1.1 - direction.1);

                // PART 1
                if in_bounds(an_plus, height, width) {
                    antinodes_part1.push(an_plus);
                }
                if in_bounds(an_min, height, width) {
                    antinodes_part1.push(an_min);
                }

                // PART 2
                antinodes_part2.push(pos1);
                antinodes_part2.push(pos2);

                // Process points in positive direction
                while in_bounds(an_plus, height, width) {
                    antinodes_part2.push(an_plus);
                    an_plus = (an_plus.0 + direction.0, an_plus.1 + direction.1);
                }

                // Process points in negative direction
                while in_bounds(an_min, height, width) {
                    antinodes_part2.push(an_min);
                    an_min = (an_min.0 - direction.0, an_min.1 - direction.1);
                }
            }
        }
    }

    // Convert to HashSet to get unique points and count
    let unique_antinodes_part1: HashSet<_> = antinodes_part1.into_iter().collect();
    let unique_antinodes_part2: HashSet<_> = antinodes_part2.into_iter().collect();

    println!("Part one: {}", unique_antinodes_part1.len());
    println!("Part two: {}", unique_antinodes_part2.len());
}