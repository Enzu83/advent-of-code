package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

var dir_to_delta = map[string][2]int {
	"R": {1, 0},
	"L": {-1, 0},
	"U": {0, -1},
	"D": {0, 1},
}

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
	input := strings.Split(getInput("input.txt"), "\n")

	wire_1_locations := listPathLocations([2]int{0, 0}, strings.Split(input[0], ","))
	wire_2_locations := listPathLocations([2]int{0, 0}, strings.Split(input[1], ","))

	intersections := [][2]int{}

	for wire_1_position := range wire_1_locations {
		_, exists := wire_2_locations[wire_1_position]

		if exists {
			intersections = append(intersections, wire_1_position)
		}
	}

	fmt.Printf("Nearest intersection distance: %d", shortestDistance(intersections))
}

// Code for part 2
func part2() {

}

func listPathLocations(position [2]int, instructions []string) map[[2]int]bool {
	locations := make(map[[2]int]bool)

	for _, instruction := range instructions {
		delta := dir_to_delta[instruction[:1]]
		amount, err := strconv.Atoi(instruction[1:])

		if err != nil {
			panic(err)
		}

		for range amount {
			position[0] += delta[0]
			position[1] += delta[1]

			locations[position] = true
		}
	}

	return locations
}

func manhattanDistance(point_1, point_2 [2]int) int {
	// abs(x) = max(x, -x)
	return max(point_1[0] - point_2[0], point_2[0] - point_1[0]) + max(point_1[1] - point_2[1], point_2[1] - point_1[1])
}

func shortestDistance(locations [][2]int) int {
	if len(locations) == 0 {
		panic("Empty locations slice, cannot find minimum.")
	}

	shortest_distance := manhattanDistance(locations[0], [2]int{0, 0})

	for _, value := range locations {
		distance := manhattanDistance(value, [2]int{0, 0})

		if distance < shortest_distance {
			shortest_distance = distance
		}
	}

	return shortest_distance
}
