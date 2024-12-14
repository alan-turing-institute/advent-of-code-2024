use std::env;
use std::fs;
use std::io::Write;

const SPACE_WIDTH: i32 = 101;
const SPACE_HEIGHT: i32 = 103;
const RUN_TIME: i32 = 100;

fn main() {

    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    println!("Using file {}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut robots = parse_file(&contents);

    println!("Part one: {}", part_one(&mut robots));

    let mut robots = parse_file(&contents); // reset starting positions
    part_two(&mut robots);
}

#[derive(Debug, Clone)]
struct Robot {
    p_x: i32,
    p_y: i32,
    v_x: i32,
    v_y: i32,
}

fn parse_file(contents: &str) -> Vec<Robot> {
    let mut robots = Vec::new();

    for line in contents.lines() {
        let parts: Vec<i32> = line
            .split(&['p', '=', ' ', 'v', ','][..])
            .filter_map(|s| s.trim().parse().ok())
            .collect();
        if parts.len() == 4 {
            let (p_x, p_y, v_x, v_y) = (parts[0], parts[1], parts[2], parts[3]);
            robots.push(Robot { p_x, p_y, v_x, v_y });
        }
    }

    robots
}

fn part_one(robots: &mut Vec<Robot>) -> i32 {

    // take 100 steps. robots wrap around edges of the space
    // for _ in 0..RUN_TIME {

    for robot in robots.iter_mut() {
        robot.p_x = (robot.p_x + RUN_TIME * robot.v_x).rem_euclid(SPACE_WIDTH);
        robot.p_y = (robot.p_y + RUN_TIME * robot.v_y).rem_euclid(SPACE_HEIGHT);
    }

    // count number of robots in each quadrant and multiply.
    // robots on centre line are ignored
    let mut top_left = 0;
    let mut top_right = 0;
    let mut bottom_left = 0;
    let mut bottom_right = 0;

    for robot in robots.iter() {
        // println!("{:?}", robot);
        if robot.p_x < SPACE_WIDTH / 2 && robot.p_y < SPACE_HEIGHT / 2 {
            top_left += 1;
        } else if robot.p_x >= SPACE_WIDTH / 2 + 1 && robot.p_y < SPACE_HEIGHT / 2 {
            top_right += 1;
        } else if robot.p_x < SPACE_WIDTH / 2 && robot.p_y >= SPACE_HEIGHT / 2 + 1 {
            bottom_left += 1;
        } else if robot.p_x >= SPACE_WIDTH / 2 + 1 && robot.p_y >= SPACE_HEIGHT / 2 + 1 {
            bottom_right += 1;
        }
    }

    top_left * top_right * bottom_left * bottom_right
}

fn part_two(robots: &mut Vec<Robot>) {
    // Create images directory if it doesn't exist
    fs::create_dir_all("images").expect("Failed to create images directory");

    for step in 1..10000 {
        let mut space = vec![vec![0_i32; SPACE_WIDTH as usize]; SPACE_HEIGHT as usize];

        // Update robot positions
        for robot in robots.iter_mut() {
            robot.p_x = (robot.p_x + robot.v_x).rem_euclid(SPACE_WIDTH);
            robot.p_y = (robot.p_y + robot.v_y).rem_euclid(SPACE_HEIGHT);
        }

        // Build grid
        for robot in robots.iter() {
            space[robot.p_y as usize][robot.p_x as usize] += 1;
        }

        // Write PBM file for this step
        let filename = format!("images/step_{:06}.pbm", step);
        let mut file = fs::File::create(filename).expect("Failed to create file");

        // Write header
        writeln!(file, "P1").expect("Failed to write header");
        writeln!(file, "{} {}", SPACE_WIDTH, SPACE_HEIGHT).expect("Failed to write dimensions");

        // Write grid data
        for row in space {
            let row_str: String = row.iter()
                .map(|&c| if c == 0 { "0" } else { "1" })
                .collect::<Vec<&str>>()
                .join(" ");
            writeln!(file, "{}", row_str).expect("Failed to write row");
        }

        // Optional: Print progress every 1000 steps
        if step % 1000 == 0 {
            println!("Processed step {}", step);
        }
    }
}