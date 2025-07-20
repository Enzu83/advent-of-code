# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def countXMAS(grid, row, col):
    xmas_number = 0

    # Check for XMAS in 8-directions

    if col >= 3:
        # top-left
        if row >= 3 and grid[row-1][col-1] + grid[row-2][col-2] + grid[row-3][col-3] == "MAS":
            xmas_number += 1
        
        # top
        if grid[row][col-1] + grid[row][col-2] + grid[row][col-3] == "MAS":
            xmas_number += 1
        
        # top-right
        if row <= len(grid)-4 and grid[row+1][col-1] + grid[row+2][col-2] + grid[row+3][col-3] == "MAS":
            xmas_number += 1
    

    if col <= len(grid[0])-4:
        # bottom-right
        if row <= len(grid)-4 and grid[row+1][col+1] + grid[row+2][col+2] + grid[row+3][col+3] == "MAS":
            xmas_number += 1

        # bottom
        if grid[row][col+1] + grid[row][col+2] + grid[row][col+3] == "MAS":
            xmas_number += 1
        
        # bottom-left
        if row >= 3 and grid[row-1][col+1] + grid[row-2][col+2] + grid[row-3][col+3] == "MAS":
            xmas_number += 1

    # right
    if row <= len(grid)-4 and grid[row+1][col] + grid[row+2][col] + grid[row+3][col] == "MAS":
        xmas_number += 1


    # left
    if row >= 3 and grid[row-1][col] + grid[row-2][col] + grid[row-3][col] == "MAS":
        xmas_number += 1

    return xmas_number


def findAllXMAS(grid):
    xmas_number = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'X':
                xmas_number += countXMAS(grid, row, col)
    
    return xmas_number

# Code

print(findAllXMAS(input_data))