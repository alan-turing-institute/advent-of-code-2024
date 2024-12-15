use std::env;
use std::fs;

fn main() {

    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let (mut grid, directions) = parse_file(&contents);

    // pretty print grid
    // for row in &grid {
    //     for c in row {
    //         print!("{}", c);
    //     }
    //     println!();
    // }
    // println!("Directions: {:?}", directions);

    println!("Part one: {}", part_one(&mut grid, &directions));
    let (mut grid, directions) = parse_file(&contents);
    println!("Part two: {}", part_two(&grid, &directions));
}

fn parse_file(contents: &str) -> (Vec<Vec<char>>, Vec<(char)>) {
    let mut grid = Vec::new();
    let mut directions = Vec::new();

    // split on empty line into two parts
    let parts: Vec<&str> = contents.split("\n\n").collect();

    // parse grid
    for line in parts[0].lines() {
        let row: Vec<char> = line.chars().collect();
        grid.push(row);
    }

    // parse directions - although split over multiple lines, treat as one long sequence
    for line in parts[1].lines() {
        for c in line.chars() {
            directions.push(c);
        }
    }

    (grid, directions)
}

fn try_to_move(mut grid: Vec<Vec<char>>, robot_pos: (usize, usize), dx: i64, dy: i64) -> (Vec<Vec<char>>, (usize, usize)) {
    let (row, col) = robot_pos;
    let new_row = (row as i64 + dx) as usize;
    let new_col = (col as i64 + dy) as usize;

    // Check if new position is within bounds and not a wall
    if new_row >= grid.len() || new_col >= grid[0].len() || grid[new_row][new_col] == '#' {
        return (grid, robot_pos);
    }

    // If the new position is empty, simply move the robot
    if grid[new_row][new_col] == '.' {
        grid[row][col] = '.';
        grid[new_row][new_col] = '@';
        return (grid, (new_row, new_col));
    }

    // If there's a box, we need to check if we can push it
    if grid[new_row][new_col] == 'O' {
        let mut boxes_to_push = vec![(new_row, new_col)];
        let mut current_pos = (new_row as i64, new_col as i64);

        // Find all consecutive boxes in the push direction
        loop {
            current_pos = (current_pos.0 + dx, current_pos.1 + dy);

            // Check bounds
            if current_pos.0 < 0 || current_pos.1 < 0 ||
               current_pos.0 >= grid.len() as i64 ||
               current_pos.1 >= grid[0].len() as i64 {
                return (grid, robot_pos);
            }

            let cur_char = grid[current_pos.0 as usize][current_pos.1 as usize];
            if cur_char == '#' {
                return (grid, robot_pos); // Can't push into wall
            }
            if cur_char == 'O' {
                boxes_to_push.push((current_pos.0 as usize, current_pos.1 as usize));
            }
            if cur_char == '.' {
                break; // Found empty space
            }
        }

        // Move all boxes one space in the push direction
        for &(box_row, box_col) in boxes_to_push.iter().rev() {
            grid[box_row][box_col] = '.';
            grid[(box_row as i64 + dx) as usize][(box_col as i64 + dy) as usize] = 'O';
        }

        // Move robot to the vacated space
        grid[row][col] = '.';
        grid[new_row][new_col] = '@';
        return (grid, (new_row, new_col));
    }

    (grid, robot_pos)
}

fn try_to_move_wide(mut grid: Vec<Vec<char>>, robot_pos: (usize, usize), dx: i64, dy: i64) -> (Vec<Vec<char>>, (usize, usize)) {
    (grid, robot_pos)
}

fn scale_up_map(grid: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut wide_grid = Vec::new();

    for row in grid {
        let mut new_row = Vec::new();
        for &c in row {
            match c {
                '#' => {
                    new_row.push('#');
                    new_row.push('#');
                }
                'O' => {
                    new_row.push('[');
                    new_row.push(']');
                }
                '.' => {
                    new_row.push('.');
                    new_row.push('.');
                }
                '@' => {
                    new_row.push('@');
                    new_row.push('.');
                }
                _ => panic!("Invalid character in grid"),
            }
        }
        wide_grid.push(new_row);
    }

    wide_grid
}

fn calculate_gps_coordinates(grid: &Vec<Vec<char>>) -> i64 {
    let mut sum = 0;
    for (i, row) in grid.iter().enumerate() {
        for (j, _) in row.iter().enumerate() {
            if j + 1 < row.len() && row[j] == '[' && row[j + 1] == ']' {
                sum += (100 * i + j) as i64;
            }
        }
    }
    sum
}

fn part_one(grid: &mut Vec<Vec<char>>, directions: &Vec<char>) -> i64 {
    let mut robot_pos = (0, 0);
    for (i, row) in grid.iter().enumerate() {
        for (j, c) in row.iter().enumerate() {
            if *c == '@' {
                robot_pos = (i, j);
                break;
            }
        }
    }

    let mut current_grid = grid.clone();
    for &dir in directions {
        let (dx, dy) = match dir {
            '^' => (-1, 0),
            'v' => (1, 0),
            '<' => (0, -1),
            '>' => (0, 1),
            _ => panic!("Invalid direction"),
        };

        let (new_grid, new_pos) = try_to_move(current_grid, robot_pos, dx, dy);
        current_grid = new_grid;
        robot_pos = new_pos;
    }

    let mut sum = 0;
    for (i, row) in current_grid.iter().enumerate() {
        for (j, c) in row.iter().enumerate() {
            if *c == 'O' {
                sum += (100 * i + j) as i64;
            }
        }
    }

    sum
}

fn part_two(grid: &Vec<Vec<char>>, directions: &Vec<char>) -> i64 {
    let mut wide_grid = scale_up_map(grid);

    let mut robot_pos = (0, 0);
    for (i, row) in wide_grid.iter().enumerate() {
        for (j, c) in row.iter().enumerate() {
            if *c == '@' {
                robot_pos = (i, j);
                break;
            }
        }
    }

    let mut current_grid = wide_grid;
    for &dir in directions {
        println!("Move {}:", dir);
        let (dx, dy) = match dir {
            '^' => (-1, 0),
            'v' => (1, 0),
            '<' => (0, -1),
            '>' => (0, 1),
            _ => panic!("Invalid direction"),
        };

        let (new_grid, new_pos) = try_to_move_wide(current_grid, robot_pos, dx, dy);
        current_grid = new_grid;
        robot_pos = new_pos;

        // pretty print grid
        for row in &current_grid {
            for c in row {
                print!("{}", c);
            }
            println!();
        }
    }

    calculate_gps_coordinates(&current_grid)
}