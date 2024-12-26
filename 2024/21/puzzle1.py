# Custom input
input_data = """029A
980A
179A
456A
379A"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

num_grid = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [None, '0', 'A']]
dir_grid = [[None, '^', 'A'], ['<', 'v', '>']]

num_dir = {
    '7': ">v",      '8': "<>v",     '9': "<v",
    '4': ">^v",     '5': "<>^v",    '6': "<^v",
    '1': ">^",      '2': "<>^v",    '3': "<^v",
                    '0': ">^",      'A': "<^",
}

dir_seq = {
    'A': {'A': [""], '^': ["<"], '>': ["v"], 'v': ["<v", "v<"], '<': ["<v<", "v<<"]},
    '^': {'A': [">"], '^': [""], '>': [">v", "v>"], 'v': ["v"], '<': ["v<"]},
    '>': {'A': ["^"], '^': ["<^", "^<"], '>': [""], 'v': ["<"], '<': ["<<"]},
    'v': {'A': [">^", "^>"], '^': ["^"], '>': [">"], 'v': [""], '<': ["<"]},
    '<': {'A': [">^>", ">>^"], '^': [">^"], '>': [">>"], 'v': [">"], '<': [""]},
}

dir_to_delta = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0)
}

# Functions

def exploreSequences(dir_robots):
    moves = {} # {02: "<vA<AA>>^A"}

    pos = ['A'] * (dir_robots + 1) # [dir_pos, num_pos]

    # dfs
    stack = [(pos[0], 0)] # [(position, robot)]

    while stack:
        current_pos, robot = stack.pop()


def findCoordinates(pos, grid):
    for y in range(len(grid)):
        for x, cell in enumerate(grid[y]):
            if cell == pos:
                return (y, x)

def getPossibleDirections(grid, start, end):
    possible_dirs = set()

    start = findCoordinates(start, grid)
    end = findCoordinates(end, grid)

    dy = end[0] - start[0]
    dx = end[1] - start[1]

    if dy > 0:
        possible_dirs.add('v')
    elif dy < 0:
        possible_dirs.add('^')
    
    if dx > 0:
        possible_dirs.add('>')
    elif dx < 0:
        possible_dirs.add('<')
    
    return possible_dirs

def nextPos(current, dir, grid):
    coordinates = findCoordinates(current, grid)
    delta = dir_to_delta[dir]

    return grid[coordinates[0] + delta[0]][coordinates[1] + delta[1]]

def findNumSequences(start, end):
    sequences = []

    # dfs
    stack = [(start, "")]

    possible_dirs = getPossibleDirections(num_grid, start, end)

    while stack:
        pos, seq = stack.pop()

        if pos == end:
            sequences.append(seq + 'A')
        else:
            for dir in num_dir[pos]:
                if dir in possible_dirs and nextPos(pos, dir, num_grid) is not None:
                    stack.append((nextPos(pos, dir, num_grid), seq + dir))
    
    return sequences
 

def findDirSequences(prev_seqs):
    sequences = []

    # dfs
    stack = [('A', list(prev_seq), "") for prev_seq in prev_seqs]

    while stack:
        pos, remaining_dirs, seq = stack.pop()

        if len(remaining_dirs) == 0:
            sequences.append(seq)
        else:
            next_pos = remaining_dirs.pop(0)

            for dir in dir_seq[pos][next_pos]:
                stack.append((next_pos, remaining_dirs.copy(), seq + dir + 'A'))
    
    minimum = min(map(len, sequences))

    return [seq for seq in sequences if len(seq) == minimum]


def getTotalLength(code, dir_robots):
    code = ['A'] + list(code)
    sequences = []

    total_length = 0

    for i in range(1, len(code)):
        sequences = findNumSequences(code[i-1], code[i])

        for _ in range(dir_robots):
            sequences = findDirSequences(sequences)
        
        total_length += len(sequences[0])
    
    return total_length

def getTotalComplexity(codes, dir_robots):
    complexity = 0

    for code in codes:
        complexity += int(code[:-1]) * getTotalLength(code, dir_robots)
    
    return complexity

# Code

print(getTotalComplexity(input_data, 2))