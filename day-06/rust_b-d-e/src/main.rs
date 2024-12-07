use std::env;
use std::fs;
use std::collections::HashSet;

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

    // debug print
    // println!("{:?}", input);

    println!("Part one: {:?}", part_one(&input));
    println!("Part two: {:?}", part_two(&input));
}

#[derive(Debug, Clone)]
struct Guard {
    row: usize,
    col: usize,
    direction: char,
}

impl Guard {
    fn get_next_position(&self) -> (i32, i32) {
        match self.direction {
            '^' => (self.row as i32 - 1, self.col as i32),
            '>' => (self.row as i32, self.col as i32 + 1),
            'v' => (self.row as i32 + 1, self.col as i32),
            '<' => (self.row as i32, self.col as i32 - 1),
            _ => panic!("Invalid direction"),
        }
    }

    fn turn_right(&mut self) {
        self.direction = match self.direction {
            '^' => '>',
            '>' => 'v',
            'v' => '<',
            '<' => '^',
            _ => panic!("Invalid direction"),
        };
    }
}

fn find_guard(input: &Vec<Vec<char>>) -> Option<Guard> {
    let guard_chars = ['^', '>', 'v', '<'];

    for (row_idx, row) in input.iter().enumerate() {
        for (col_idx, &cell) in row.iter().enumerate() {
            if guard_chars.contains(&cell) {
                return Some(Guard {
                    row: row_idx,
                    col: col_idx,
                    direction: cell,
                });
            }
        }
    }
    None
}

fn is_in_bounds(row: i32, col: i32, rows: i32, cols: i32) -> bool {
    row >= 0 && row < rows && col >= 0 && col < cols
}

fn count_x(grid: &Vec<Vec<char>>) -> i32 {
    let mut count = 0;
    for row in grid {
        for &cell in row {
            if cell == 'X' {
                count += 1;
            }
        }
    }
    count
}

fn part_one(input: &Vec<Vec<char>>) -> i32 {
    let rows = input.len() as i32;
    let cols = input[0].len() as i32;

    let mut guard = match find_guard(input) {
        Some(g) => g,
        None => {
            println!("No guard found in input!");
            return 0;
        }
    };

    // Create a mutable copy of the input grid
    let mut grid = input.clone();

    // Mark initial position with X
    grid[guard.row][guard.col] = 'X';

    // Continue until we leave the grid
    loop {
        // Get next position
        let (next_row, next_col) = guard.get_next_position();

        // If we're out of bounds or hit a wall, turn right
        if !is_in_bounds(next_row, next_col, rows, cols) ||
           grid[next_row as usize][next_col as usize] == '#' {
            guard.turn_right();
            continue;
        }

        // Move to next position and mark it
        guard.row = next_row as usize;
        guard.col = next_col as usize;
        grid[guard.row][guard.col] = 'X';

        // If we're at the edge of the grid, we're done
        if guard.row == 0 || guard.row == (rows-1) as usize ||
           guard.col == 0 || guard.col == (cols-1) as usize {
            break;
        }
    }

    count_x(&grid)
}

fn part_two(input: &Vec<Vec<char>>) -> i32 {
    let rows = input.len() as i32;
    let cols = input[0].len() as i32;

    // Find initial guard position
    let initial_guard = match find_guard(input) {
        Some(g) => g,
        None => {
            println!("No guard found in input!");
            return 0;
        }
    };

    // First, find all positions the guard will visit
    let mut guard = initial_guard.clone();
    let mut path_positions = HashSet::new();
    let grid = input.clone();

    // Get the guard's path until it leaves the grid
    loop {
        let (next_row, next_col) = guard.get_next_position();

        if !is_in_bounds(next_row, next_col, rows, cols) ||
           grid[next_row as usize][next_col as usize] == '#' {
            guard.turn_right();
            continue;
        }

        guard.row = next_row as usize;
        guard.col = next_col as usize;
        path_positions.insert((guard.row, guard.col));

        if guard.row == 0 || guard.row == (rows-1) as usize ||
           guard.col == 0 || guard.col == (cols-1) as usize {
            break;
        }
    }

    let mut loop_positions = 0;

    // Only test positions that the guard would visit
    for &(row, col) in &path_positions {
        // Skip the guard's starting position
        if row == initial_guard.row && col == initial_guard.col {
            continue;
        }

        // Create a new grid with an obstacle at this position
        let mut test_grid = input.clone();
        test_grid[row][col] = '#';

        // Test if this creates a loop
        if creates_loop(&test_grid, initial_guard.clone()) {
            loop_positions += 1;
        }
    }

    loop_positions
}

fn creates_loop(grid: &Vec<Vec<char>>, initial_guard: Guard) -> bool {
    let rows = grid.len() as i32;
    let cols = grid[0].len() as i32;
    let mut guard = initial_guard;
    let mut visited = HashSet::new();

    // Add initial position and direction to visited
    visited.insert((guard.row, guard.col, guard.direction));

    loop {
        let (next_row, next_col) = guard.get_next_position();

        // If we hit a wall or boundary, turn right
        if !is_in_bounds(next_row, next_col, rows, cols) ||
           grid[next_row as usize][next_col as usize] == '#' {
            guard.turn_right();

            // If we've seen this position and direction before, it's a loop
            if visited.contains(&(guard.row, guard.col, guard.direction)) {
                return true;
            }

            visited.insert((guard.row, guard.col, guard.direction));
            continue;
        }

        // Move to next position
        guard.row = next_row as usize;
        guard.col = next_col as usize;

        // If we've seen this position and direction before, it's a loop
        if visited.contains(&(guard.row, guard.col, guard.direction)) {
            return true;
        }

        // If we're at the edge of the grid, it's not a loop
        if guard.row == 0 || guard.row == (rows-1) as usize ||
           guard.col == 0 || guard.col == (cols-1) as usize {
            return false;
        }

        visited.insert((guard.row, guard.col, guard.direction));
    }
}