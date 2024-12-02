use std::fs;

fn check_safe_1(report: &Vec<i64>) -> bool {
   let mut diff = report[1] - report[0];
   if (diff.abs() < 1) || (diff.abs() > 3) {
      return false;
   }
   for i in 2..report.len() {
       let new_diff = report[i] - report[i-1];
       if diff * new_diff < 0 {
       	  return false;
       }
       if (new_diff.abs() < 1) || (new_diff.abs() > 3) {
       	  return false;
       }
       diff = new_diff;

   }
   return true;
}


fn check_safe_2(report: &Vec<i64>) -> bool {
   let mut num_unsafe = 0;
   let mut diff = report[1] - report[0];
   if (diff.abs() < 1) || (diff.abs() > 3) {
      num_unsafe +=1;
   }
   for i in 2..report.len() {
       let new_diff = report[i] - report[i-1];
       if diff * new_diff < 0 {
       	  num_unsafe += 1
       } else if (new_diff.abs() < 1) || (new_diff.abs() > 3) {
       	  num_unsafe += 1
       } else {
          diff = new_diff;
       }
       if num_unsafe > 1 {
       	  return false;
       }

   }
   return true;
}

fn main() {

    let contents = fs::read_to_string("input.txt")
       .expect("Should be able to read file");
    let mut num_safe_1 = 0;
    let mut num_safe_2 = 0;
    for line in contents.lines() {
    	let report: Vec<i64> = line.split_whitespace()
				    .map(|s| s.parse::<i64>().unwrap())
				    .collect();
    	if check_safe_1(&report) {
	   num_safe_1 += 1;
	}
	if check_safe_2(&report) {
	   num_safe_2 += 1;
	}
    }
    println!("part 1: {num_safe_1}");
    println!("part 2: {num_safe_2}");

}
