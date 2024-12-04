package main

import (
  "fmt"
  "os"
  "strings"
  "strconv"
  "bufio"
)

func ReadNumbersFromFile(fpath string) ([][]int, error) {

  // open file and check
  file, err := os.Open(fpath)
  if err != nil {
		return nil, err
	}
  defer file.Close()

  // Setup output slice
  var result [][]int

  // Read line by line
  scanner := bufio.NewScanner(file)
  for scanner.Scan() {

    rawFields := strings.Fields(scanner.Text())

    // Parse each number in the line
    var numbers []int
    for _, field := range rawFields {
      n, _ := strconv.Atoi(field)
      numbers = append(numbers, n)
    }

    // Add to the total result
    result = append(result, numbers)
  }

  return result, nil
}

func IsReportSafe(report []int) bool {

  if len(report) < 2 { return true }

  var previous int = report[0]
  var delta int = 0
  var increasing bool = report[1] > report[0]

  for i, level := range report {

    // Skip first
    if i == 0 { continue }
    delta = level-previous

    // Unsafe if no change
    if delta == 0 { return false }

    // Check unsafe delta
    if delta < -3 || delta > 3 { return false }

    // Check if consistently increasing or decreasing
    if  increasing && delta < 0 { return false }
    if !increasing && delta > 0 { return false }

    previous = level
  }

  return true
}

// This one doesn't work  :((((
func IsReportSafeWithTol1(report []int) bool {

  if len(report) < 2 { return true }
  if IsReportSafe(report[1:]) { return true }

  var previous int = report[0]
  var delta int = 0
  var increasing bool = report[1] > report[0]

  var skipAvailable bool = true
  var badLevel bool

  for i, level := range report {

    // Skip first
    if i == 0 { continue }
    badLevel = false
    delta = level-previous

    // Unsafe if no change
    if delta == 0 { badLevel = true }

    // Check unsafe delta
    if delta < -3 || delta > 3 { badLevel = true }

    // Check if consistently increasing or decreasing
    if  (increasing && delta < 0) || (!increasing && delta > 0) { badLevel = true }

    // Check if can skip and carry on
    if badLevel {
      if skipAvailable {
        previous = report[i-1]
        skipAvailable = false
      } else {
        return false
      }
    } else {
      previous = level
    }
  }

  return true
}

// Boo hiss brute force version :'(
func IsReportSafeWithTol2(report []int) bool {

  if len(report) < 2 { return true }

  // var length int = len(report) - 1
  // var ablatedReport []int

  for i := range len(report) {
    ablatedReport := make([]int, len(report)-1)

    copy(ablatedReport[:i], report[:i])
    copy(ablatedReport[i:], report[i+1:])
    if IsReportSafe(ablatedReport) {return true}
  }

  return false
}

func main() {

  var filename string = "input.txt"

  reports, _ := ReadNumbersFromFile(filename)

  var numSafe int = 0
  var numSafeWithTol int = 0

  for _, report := range reports {
    if IsReportSafe(report) { numSafe++ }
    if IsReportSafeWithTol2(report) { numSafeWithTol++ }
  }

  fmt.Println("Part 1: ", numSafe, " reports are safe.")
  fmt.Println("Part 2: ", numSafeWithTol, " reports are safe with Problem Dampener.")

}
