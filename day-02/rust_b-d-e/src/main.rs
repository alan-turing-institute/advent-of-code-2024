use std::env;
use std::fs;

fn main() {
    // read in the file

    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    println!("Using file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    // each line of data is one report, of arbitary length
    // each report is a list of numbers
    // each number is separated by a space

    // split the contents into a list of reports
    let reports: Vec<&str> = contents.split("\n").collect();

    // split each report into a list of numbers
    let mut report_data: Vec<Vec<i32>> = Vec::new();
    for report in reports {
        let numbers: Vec<i32> = report.split(" ").map(|x| x.parse().unwrap()).collect();
        report_data.push(numbers);
    }

    // part one
    println!("Safe reports: {:?}", part_one(&report_data));

    // part two
    println!("Safe reports with max one error: {:?}", part_two(&report_data));
}

fn check_safe(report: &Vec<i32>) -> (bool, i32) {
    if report.len() < 2 {
        return (true, -1);
    }

    let increasing: bool = report[0] < report[1];

    for i in 0..report.len() - 1 {
        // Get difference first
        let diff = (report[i + 1] - report[i]).abs();

        // Check both conditions - if either fails, this is our violation point
        if diff < 1 || diff > 3 || (report[i] < report[i + 1]) != increasing {
            return (false, i as i32);
        }
    }

    (true, -1)
}

fn part_one(all_reports: &Vec<Vec<i32>>) -> i32 {
    // how many reports are 'safe'?
    // i.e. lists of numbers that are:
    // ((strictly increasing) OR (strictly decreasing)) AND (differ by at least 1) AND (differ by at most 3)

    let mut safe_reports: i32 = 0;

    for report in all_reports {
        safe_reports += check_safe(report).0 as i32;
    }

    safe_reports
}



fn part_two(all_reports: &Vec<Vec<i32>>) -> i32 {
    // how many reports are 'safe'?
    // i.e. lists of numbers that are:
    // ((strictly increasing) OR (strictly decreasing)) AND (differ by at least 1) AND (differ by at most 3)
    // BUT here if removing a SINGLE number from the list makes it safe, it is also safe

    let mut safe_reports: i32 = 0;

    for report in all_reports {

        // check if the report is safe
        let (safe, bad_idx) = check_safe(report);

        // if the report is not safe, check if removing the value at the bad index makes it safe
        if !safe {
            let mut new_report = report.clone();
            new_report.remove((bad_idx) as usize);
            let (mut safe, _) = check_safe(&new_report);
            // if not, also check i+1 and 0
            if !safe {
                new_report = report.clone();
                new_report.remove((bad_idx + 1) as usize);
                (safe, _) = check_safe(&new_report);

                if !safe {
                    new_report = report.clone();
                    new_report.remove(0);
                    (safe, _) = check_safe(&new_report);
                }
            }
            safe_reports += safe as i32;
        } else {
            safe_reports += 1;
        }
    }

    safe_reports
}
