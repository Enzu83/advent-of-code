# Custom input
input_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def countCrossMAS(grid, row, col):
    # Check for X-MAS

    if 0 < row < len(grid)-1 and 0 < col < len(grid[0])-1:
        if grid[row-1][col-1] + grid[row+1][col+1] in {"MS", "SM"} and grid[row+1][col-1] + grid[row-1][col+1] in {"MS", "SM"}:
            return 1
    
    return 0


def findAllXMAS(grid):
    xmas_number = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'A':
                xmas_number += countCrossMAS(grid, row, col)
    
    return xmas_number

# Code

print(findAllXMAS(input_data))