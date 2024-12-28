package main

import (
	"fmt"
	"os"
)

// Get input as a string
func getInput(path string) string {
	raw_input, err := os.ReadFile(path)

	if err != nil {
		panic(err)
	}

	str_input := string(raw_input)

	// Remove last line break if there's one
	if str_input[len(str_input)-1] == '\n' {
		str_input = str_input[:len(str_input)-1]
	}

	return str_input
}

func main() {
	// Solve part 1 or part 2
	fmt.Printf("--- Solving part %s ---\n", os.Args[1])

	switch os.Args[1] {
	case "1":
		part1()
	case "2":
		part2()
	}
}

// Code for part 1
func part1() {

}

// Code for part 2
func part2() {

}