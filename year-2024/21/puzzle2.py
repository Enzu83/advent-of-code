# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

num_grid = {
    (0, 0): '7', (0, 1): '8', (0, 2): '9',
    (1, 0): '4', (1, 1): '5', (1, 2): '6',
    (2, 0): '1', (2, 1): '2', (2, 2): '3',
                 (3, 1): '0', (3, 2): 'A',
}

dir_grid = {
                 (0, 1): '^', (0, 2): 'A',
    (1, 0): '<', (1, 1): 'v', (1, 2): '>',
}

# Functions

def buildMoves(grid):
    grid_moves = {}

    for button_pos, button_label in grid.items():
        grid_moves[button_label] = {}

        # dfs
        stack = [(button_pos, "", set())] # (current button, moves, visited buttons)

        while stack:
            current, moves, visited = stack.pop()
            visited.add(current)
            
            # add moves
            if grid[current] not in grid_moves[button_label]:
                grid_moves[button_label][grid[current]] = [moves]
            else:
                grid_moves[button_label][grid[current]].append(moves)
            
            # search neighbor buttons NWES
            if (current[0] - 1, current[1]) in grid.keys() - visited:
                stack.append(((current[0] - 1, current[1]), moves + "^", visited | {(current[0] - 1, current[1])}))
            
            if (current[0] + 1, current[1]) in grid.keys() - visited:
                stack.append(((current[0] + 1, current[1]), moves + "v", visited | {(current[0] + 1, current[1])}))
            
            if (current[0], current[1] - 1) in grid.keys() - visited:
                stack.append(((current[0], current[1] - 1), moves + "<", visited | {(current[0], current[1] - 1)}))
            
            if (current[0], current[1] + 1) in grid.keys() - visited:
                stack.append(((current[0], current[1] + 1), moves + ">", visited | {(current[0], current[1] + 1)}))
    
    # remove longer moves
    for button in grid_moves:
        for target_button, moves in grid_moves[button].items():
            minimum_move = len(min(moves, key=len))
            grid_moves[button][target_button] = [move for move in moves if len(move) == minimum_move]
    
    return grid_moves  

def length(start, end, robot=0):
    if (robot, start, end) in known_lengths:
        return known_lengths[(robot, start, end)]
    
    # for the 1st robot on the directional keypad, it gets the moves from the numeric keypad
    if robot == 0:
        moves_list = num_moves[start][end]
    else:
        moves_list = dir_moves[start][end]

    if robot == DIR_ROBOTS:
        return len(moves_list[0]) + 1 # count the 'A' press

    lengths = []

    for moves in moves_list:
        moves = 'A' + moves + 'A' # add the path from 'A' to the first move & count the 'A' press
        total_length = sum(length(moves[i-1], moves[i], robot + 1) for i in range(1, len(moves)))

        lengths.append(total_length)
    
    minimum = min(lengths)

    if (robot, start, end) not in known_lengths:
        known_lengths[(robot, start, end)] = min(lengths)

    return minimum


def codeLength(code):
    code = 'A' + code
    return sum(length(code[i-1], code[i]) for i in range(1, len(code)))

def getComplexity(codes):
    return sum(int(code[:-1]) * codeLength(code) for code in codes)

# Code

DIR_ROBOTS = 25

num_moves = buildMoves(num_grid)
dir_moves = buildMoves(dir_grid)

known_lengths = {}

print(getComplexity(input_data))