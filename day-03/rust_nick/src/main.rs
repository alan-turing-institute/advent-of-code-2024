use std::fs;
use regex::Regex;

fn part1(memory: &str) -> i64 {
   let re = Regex::new(r"mul\(([\d]+),([\d]+)\)").expect("Invalid regex");
   let mut total = 0;
   for result in re.captures_iter(memory) {
       let num1 = &result[1].parse::<i64>().unwrap();
       let num2 = &result[2].parse::<i64>().unwrap();
       total += num1 * num2;
   }
   return total;
}


fn part2(memory: &str) -> i64 {
   let mut total = 0;

   let re = Regex::new(r"mul\(([\d]+),([\d]+)\)|(don't\(\))|(do\(\))").expect("Invalid regex");
   let mut adding = true;
   for result in re.captures_iter(memory) {
       if result.get(3).map_or("N/A", |m| m.as_str()) == "don't()" {
       	  adding = false;
       } else if result.get(4).map_or("N/A", |m| m.as_str()) == "do()" {
       	  adding = true;
       } else {
          if adding {
       	     let num1 = &result[1].parse::<i64>().unwrap();
       	     let num2 = &result[2].parse::<i64>().unwrap();
       	     total += num1 * num2;
          }
       };
   }

   return total;

}

fn main() {

    let contents = fs::read_to_string("input.txt")
    	.expect("should be able to read the file");
    let part1_result = part1(&contents);
    println!("Part 1 {part1_result}");

    let part2_result = part2(&contents);
    println!("Part 2 {part2_result}");

}
