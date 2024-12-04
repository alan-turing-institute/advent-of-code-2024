package main

import (
  "fmt"
  "os"
  "regexp"
  "strconv"
)

func main() {
  var filename string = "test.txt"

  memory, _ := os.ReadFile(filename)

  pattern := regexp.MustCompile(`mul\(\d{1,3},\d{1,3}\)`)
  num_pattern := regexp.MustCompile(`\d{1,3}`)

  matches := pattern.FindAll(memory, -1)

  var total int = 0

  for _, op := range matches {
    // I wish I could do this in one line :(
    // maybe use FindAllString? but then would have had to convert everything to string earlier
    nums := num_pattern.FindAll(op, -1)
    num1, _ := strconv.Atoi(string(nums[0]))
    num2, _ := strconv.Atoi(string(nums[1]))
    total += num1 * num2
  }

  fmt.Println("Part 1: ", total)

}
