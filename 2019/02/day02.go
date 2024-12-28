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

	str_input := string(raw_input)

	// Replace all CRLF by LF
	str_input = strings.ReplaceAll(str_input, "\r\n", "\n")

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
	input := strings.Split(getInput("input.txt"), ",")
	program := stringSliceToInt(input)
	
	// Replacement before run
	program[1] = 12
	program[2] = 2

	runProgram(program)

	fmt.Printf("Value at position 0: %d\n", program[0])
}

// Code for part 2
func part2() {
	input := strings.Split(getInput("input.txt"), ",")
	default_program := stringSliceToInt(input)

	for noun := range 100 {
		for verb := range 100 {
			// Get the default program memory
			modified_program := make([]int, len(default_program))
			copy(modified_program, default_program)

			// Replacement before run
			modified_program[1] = noun
			modified_program[2] = verb

			runProgram(modified_program)

			if modified_program[0] == 19690720 {
				fmt.Printf("Answer: %d", 100 * noun + verb)
				return
			}
		}
	}
}

func stringSliceToInt(str_slice []string) []int {
	int_slice := make([]int, len(str_slice))

	for i, str_element := range str_slice {
		int_element, err := strconv.Atoi(str_element)

		if err != nil {
			panic(err)
		}

		int_slice[i] = int_element
	}

	return int_slice
}

func runProgram(program []int) []int {
	for i:= 0; i < len(program); i += 4 {
		opcode := program[i]

		switch opcode {
		// Opcode 1: Addition
		case 1:
			program[program[i+3]] = program[program[i+1]] + program[program[i+2]]

		// Opcode 2: Multiplication
		case 2:
			program[program[i+3]] = program[program[i+1]] * program[program[i+2]]

		// Opcode 99: End of program
		case 99:
			return program
		
		// Else: Unknown behavior
		default:
			panic(fmt.Sprintf("Unknown opcode encountered: %d", opcode))
		}
	}

	panic("Program didn't end properly")
}