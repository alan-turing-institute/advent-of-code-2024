use std::env;
use std::fs;

fn main() {
    // read in the file

    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    // parse input text into 2d array
    let mut input: Vec<Vec<char>> = Vec::new();
    for line in contents.lines() {
        let mut row: Vec<char> = Vec::new();
        for c in line.chars() {
            row.push(c);
        }
        input.push(row);
    }

    println!("Part one: {:?}", part_one(&input));
    println!("Part two: {:?}", part_two(&input));
}


fn part_one(grid: &Vec<Vec<char>>) -> i32 {
    let mut count = 0;
    let target = "XMAS";
    let rows = grid.len();
    let cols = grid[0].len();

    let directions = [
        // all ways we can move in the grid
        (0, 1),   // right
        (1, 0),   // down
        (1, 1),   // diagonal down-right
        (1, -1),  // diagonal down-left
        (0, -1),  // left
        (-1, 0),  // up
        (-1, -1), // diagonal up-left
        (-1, 1),  // diagonal up-right
    ];

    // Check each starting position
    for i in 0..rows {
        for j in 0..cols {
            // Try each direction from this position
            for &(di, dj) in &directions {
                let mut found = true;

                // Check if word fits in bounds in this direction
                let end_i = i as i32 + di * (target.len() as i32 - 1);
                let end_j = j as i32 + dj * (target.len() as i32 - 1);

                if end_i < 0 || end_i >= rows as i32 || end_j < 0 || end_j >= cols as i32 {
                    // this direction will spill out of the grid's bounds
                    continue;
                }

                // Check each character of the word
                // assume it matches until we find a wrong character
                for k in 0..target.len() {
                    let cur_i = (i as i32 + di * k as i32) as usize;
                    let cur_j = (j as i32 + dj * k as i32) as usize;

                    if grid[cur_i][cur_j] != target.chars().nth(k).unwrap() {
                        // wrong character
                        found = false;
                        break;
                    }
                }

                if found {
                    count += 1;
                }
            }
        }
    }

    count
}


fn part_two(grid: &Vec<Vec<char>>) -> i32 {
    let mut count = 0;
    let rows = grid.len();
    let cols = grid[0].len();

    // look out from centre - this will always be an A
    // check diagonals for MAS in any order

    // Skip edges - need at least 1 space on all sides for A
    for i in 1..rows-1 {
        for j in 1..cols-1 {
            // Check each cell that could be the center of an X-MAS pattern
            if check_xmas(grid, i, j) {
                count += 1;
            }
        }
    }
    count
}

fn check_xmas(grid: &Vec<Vec<char>>, i: usize, j: usize) -> bool {
    // Check if we have enough space in all directions
    if i == 0 || j == 0 || i >= grid.len()-1 || j >= grid[0].len()-1 {
        return false;
    }

    // Get the diagonals - parse chars into strings
    let down_right = format!("{}{}{}",
        grid[i-1][j-1],
        grid[i][j],
        grid[i+1][j+1]
    );

    let down_left = format!("{}{}{}",
        grid[i-1][j+1],
        grid[i][j],
        grid[i+1][j-1]
    );

    // Check each diagonal both ways
    let down_right_rev = down_right.chars().rev().collect::<String>();
    let down_left_rev = down_left.chars().rev().collect::<String>();

    // check if any pair of diagonals is MAS
    (is_mas(&down_right) || is_mas(&down_right_rev)) &&
    (is_mas(&down_left) || is_mas(&down_left_rev))
}

fn is_mas(s: &str) -> bool {
    s == "MAS"
}