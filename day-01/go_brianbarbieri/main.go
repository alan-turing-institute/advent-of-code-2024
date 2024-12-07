package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {

	data_example := readExample()
	data_input := readInput()

	total := solution1(data_example)
	fmt.Println("Answer for example solution 1: ", total)

	total = solution1(data_input)
	fmt.Println("Answer for input solution 1: ", total)

	total = solution2(data_example)
	fmt.Println("Answer for example solution 2: ", total)

	total = solution2(data_input)
	fmt.Println("Answer for input solution 2: ", total)
}

func openFile(filePath string) [][]int {
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return nil
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	// two int lists
	var left []int
	var right []int

	// Read each line
	for scanner.Scan() {
		line := scanner.Text() // Get the current line as a string
		// Split the line into parts and parse as integers
		parts := strings.Fields(line) // Split by whitespace
		if len(parts) == 2 {          // Ensure there are exactly two numbers
			left = append(left, toInt(parts[0]))
			right = append(right, toInt(parts[1]))
		}
	}

	return [][]int{left, right}
}

func readExample() [][]int {
	return openFile("day1/example.txt")
}

func readInput() [][]int {
	return openFile("day1/input.txt")
}

func toInt(s string) int {
	i, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return i
}

func solution1(data [][]int) int {
	sort.Ints(data[0])
	sort.Ints(data[1])
	total := 0
	for i := 0; i < len(data[0]); i++ {
		total += int(math.Abs(float64(data[0][i] - data[1][i])))
	}
	return total
}

func solution2(data [][]int) int {
	counts := make(map[int]int)
	total := 0

	for _, num := range data[1] { // count each number in right list
		counts[num]++
	}

	for _, num := range data[0] { // lookup in left list
		total += num * counts[num]
	}
	return total
}
