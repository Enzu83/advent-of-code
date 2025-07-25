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

	wire_1_locations := listPathLocations(strings.Split(input[0], ","))
	wire_2_locations := listPathLocations(strings.Split(input[1], ","))

	intersections := getIntersection(wire_1_locations, wire_2_locations)

	distance, _ := shortestDistanceAndSteps(intersections)

	fmt.Printf("Nearest intersection distance: %d", distance)
}

// Code for part 2
func part2() {
	input := strings.Split(getInput("input.txt"), "\n")

	wire_1_locations := listPathLocations(strings.Split(input[0], ","))
	wire_2_locations := listPathLocations(strings.Split(input[1], ","))

	intersections := getIntersection(wire_1_locations, wire_2_locations)

	_, steps := shortestDistanceAndSteps(intersections)

	fmt.Printf("Fewest steps to an intersection: %d", steps)
}
func listPathLocations(instructions []string) map[[2]int]int {
	locations := make(map[[2]int]int)
	point := [2]int{0, 0}

	steps := 0

	for _, instruction := range instructions {
		delta := dir_to_delta[instruction[:1]]
		amount, err := strconv.Atoi(instruction[1:])

		if err != nil {
			panic(err)
		}

		for range amount {
			steps += 1
			point[0] += delta[0]
			point[1] += delta[1]
			locations[point] = steps // steps from the start
		}
	}

	return locations
}

func getIntersection(locations_1, locations_2 map[[2]int]int) map[[2]int]int {
	intersections := make(map[[2]int]int) // intersections[point] = steps

	for point := range locations_1 {
		_, exists := locations_2[point]

		if exists {
			intersections[point] = locations_1[point] + locations_2[point]
		}
	}

	return intersections
}

func manhattanDistance(point_1, point_2 [2]int) int {
	// abs(x) = max(x, -x)
	return max(point_1[0] - point_2[0], point_2[0] - point_1[0]) + max(point_1[1] - point_2[1], point_2[1] - point_1[1])
}

func shortestDistanceAndSteps(locations map[[2]int]int) (int, int) {
	if len(locations) == 0 {
		panic("Empty locations, cannot find minimum distance.")
	}

	shortest_distance := 0
	shortest_steps := 0

	for point := range locations {
		distance := manhattanDistance(point, [2]int{0, 0})

		if locations[point] < shortest_steps || shortest_steps == 0 {
			shortest_steps = locations[point]
		}

		if distance < shortest_distance || shortest_distance == 0 {
			shortest_distance = distance
		}
	}

	return shortest_distance, shortest_steps
}
