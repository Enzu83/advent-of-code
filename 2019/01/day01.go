package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Get input as a string
func getInput(path string) string {
	raw_input, err := os.ReadFile(path)

	if err != nil {
		panic(err)
	}

	str_input := string(raw_input) // Remove last line break for easier later splits
	return str_input[:len(str_input)-1]
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
	input := strings.Split(getInput("input.txt"), "\n")

	var total_fuel int

	for _, line := range input {
		mass, err := strconv.Atoi(line)

		if err != nil {
			panic(err)
		}

		total_fuel += requiredFuel(mass)
	}

	fmt.Printf("Total fuel required: %d\n", total_fuel)
}

// Code for part 2
func part2() {
	input := strings.Split(getInput("input.txt"), "\n")

	var total_fuel int

	for _, line := range input {
		mass, err := strconv.Atoi(line)

		if err != nil {
			panic(err)
		}

		total_fuel += recursiveRequiredFuel(mass)
		
	}

	fmt.Printf("Total fuel required: %d\n", total_fuel)
}

func requiredFuel(mass int) int {
	return mass / 3 - 2
}

func recursiveRequiredFuel(mass int) int {
	fuel := mass / 3 - 2

	if fuel <= 0 {
		return 0
	} else {
		return fuel + recursiveRequiredFuel(fuel)
	}
}