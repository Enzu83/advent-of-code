# Custom input
input_data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting
antennas = {}

for j in range(len(input_data)):
    for i, char in enumerate(input_data[j]):
        if char != '.':
            if char not in antennas:
                antennas[char] = [(i, j)]
            else:
                antennas[char].append((i, j))


# Functions

def getAntinodeLocations(antennas, grid_size):
    antinodes = set()

    for frequency in antennas:
        # iterate over all frequency locations
        for first_position in antennas[frequency]:
            # iterate over all other frequency locations except the currently one
            for second_position in antennas[frequency]:
                # check if it's a different one
                if first_position != second_position:
                    # antinode position by translation
                    translation_step = (second_position[0] - first_position[0], second_position[1] - first_position[1])
                    antinode_position = (first_position[0], first_position[1])

                    # translate while it's still in bounds
                    while 0 <= antinode_position[0] < grid_size[0] and 0 <= antinode_position[1] < grid_size[1]:
                        antinodes.add(antinode_position) # add the antinode position to the set
                        
                        antinode_position = (antinode_position[0] - translation_step[0], antinode_position[1] - translation_step[1]) # translate the position

    return antinodes

# Code

grid_size = (len(input_data[0]), len(input_data))
antinodes = getAntinodeLocations(antennas, grid_size)

print(len(antinodes))