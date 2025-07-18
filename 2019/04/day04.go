package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Get input as a string
func getInput(path string) string {
	raw_input, e := os.ReadFile(path)
	if e != nil {
		panic(e)
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
	start, end := getRange(getInput("input.txt")) // Get password range from the input file
	fmt.Printf("Valid passwords: %d\n", countValidPassword(start, end, false)) // Count every valid password
}

// Code for part 2
func part2() {
	start, end := getRange(getInput("input.txt")) // Get password range from the input file
	fmt.Printf("Valid passwords: %d\n", countValidPassword(start, end, true)) // Count every valid password

	fmt.Println(checkValidPassword(111111, true))
	fmt.Println(checkValidPassword(223450, true))
	fmt.Println(checkValidPassword(123789, true))
	fmt.Println(checkValidPassword(112233, true))
	fmt.Println(checkValidPassword(123444, true))
	fmt.Println(checkValidPassword(111122, true))
}

func getRange(input string) (int, int) {
	values := strings.Split(input, "-")
	if len(values) > 2 {
		panic("Incorrect input, split resulted in more than 2 values")
	}

	start, e := strconv.Atoi(values[0])
	if e != nil {
		panic(e)
	}

	end, e := strconv.Atoi(values[1])
	if e != nil {
		panic(e)
	}

	return start, end
}

func checkValidPassword(password int, group_check bool) bool {
	identical_adjacent := false // flag to remember if there was two adjacent digits

	password_str := strconv.Itoa(password)

	// evaluate a candidate
	i := 0
	for range len(password_str)-1 {
		if i >= len(password_str)-1 {
			break
		}

		current_digit := password_str[i]
		next_digit := password_str[i+1]

		// never decrease check
		if current_digit > next_digit {
			return false
		}

		// two adjacent digits identical check
		if current_digit == next_digit {
			identical_adjacent = true

			// check for larger group if flag is enabled
			if group_check {

				// count digit group length
				group_length := 2

				for j := i+2; j < len(password_str); j++ {
					if password_str[j] != current_digit {
						break
					} else {
						group_length++
					}
				}
				
				// group with odd length doesn't pass the check
				if group_length % 2 == 1 {
					return false
				}

				i += group_length-1
			}
		}

		i++
	}

	return identical_adjacent
}

func countValidPassword(start int, end int, group_check bool) int {
	valid_candidates := 0

	for candidate := start; candidate <= end; candidate++ {
		if checkValidPassword(candidate, group_check) {
			valid_candidates++
		}
	}

	return valid_candidates
}