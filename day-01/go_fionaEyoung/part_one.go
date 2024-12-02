package main

import (
  "fmt"
  "os"
  // "io"
  // "encoding/csv"
  "strings"
  "strconv"
  "bufio"
  "slices"
  "errors"
)

func ReadNumbersFromFile(fpath string) ([]int, []int, error) {

  // open file and check
  file, err := os.Open(fpath)
  if err != nil {
		return nil, nil, err
	}
  defer file.Close()

  // Setup output slice
  var result1, result2 []int

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
    result1 = append(result1, numbers[0])
    result2 = append(result2, numbers[1])

  }

  return result1, result2, nil
}

// no checking if lengths are the same :(
func SubtractSlicesAbsolute(slice1, slice2 []int) ([]int, error) {

  var result []int

  if len(slice1) == len(slice2) {
    for i := range slice1 {
      if slice1[i] > slice2[i] {
        result = append(result, slice1[i]-slice2[i])
      } else {
        result = append(result, slice2[i]-slice1[i])
      }
    }
    return result, nil
  } else {
    return nil, errors.New("Slices are not the same lengths!")
  }
}

func SimilarityScore(slice1, slice2 []int) (int) {

  var score int = 0

  for _, num := range slice1 {
    var multiplier int = 0
    for _, num2 := range slice2 {
      if num2 == num {multiplier += 1}
    }
    score += num * multiplier
  }

  return score
}

func main() {

  ids1, ids2, _ := ReadNumbersFromFile("input.txt")

  // fmt.Println("First list: ", ids1)
  // fmt.Println("Second list: ", ids2)

  slices.Sort(ids1)
  slices.Sort(ids2)

  distances, _ := SubtractSlicesAbsolute(ids1, ids2)

  var result int

  for _, num := range distances {
    result += num
  }

  fmt.Println("Part 1: ", result)

  fmt.Println("Part 2: ", SimilarityScore(ids1, ids2))

}
